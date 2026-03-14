"""
Live Session Router — TRUE AGENT with Tool Calling
===================================================
The Live Tutor is a real AI agent that:
1. Receives student voice/text
2. Gemini AUTONOMOUSLY decides which tools to call
3. Backend executes the tools
4. Results are fed back to Gemini
5. Gemini responds to the student with the combined knowledge

Tools available to the agent:
- generate_quiz: Create quiz questions on any topic
- lookup_word: Dictionary lookup with etymology, IPA, analogies
- generate_visual: Create visual explanation diagrams
- analyze_page: Analyze the current textbook page
- create_bookmark: Save important concepts for revision
- suggest_next_topic: Recommend what to study next

This uses the Gemini Live API (WebSocket) with tool declarations.
"""
import os
import json
import asyncio
import base64
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from google import genai
from google.genai import types
from services.gemini_client import get_client
from config.models import TEXT_MODEL, IMAGE_MODEL, LIVE_MODEL

router = APIRouter()

# ═══════════════════════════════════════════════
# Tool Declarations — Gemini decides when to call
# ═══════════════════════════════════════════════
AGENT_TOOLS = [
    types.Tool(function_declarations=[
        types.FunctionDeclaration(
            name="generate_quiz",
            description=(
                "Generate quiz questions to test the student's understanding of a topic. "
                "Call this when: the student finishes reading a section, asks to be tested, "
                "or you want to check comprehension after explaining something."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "topic": types.Schema(type="STRING", description="The topic to quiz on"),
                    "num_questions": types.Schema(type="INTEGER", description="Number of questions (2-5)"),
                    "quiz_type": types.Schema(
                        type="STRING",
                        description="Type: mcq, fill_blank, true_false, match_following",
                    ),
                    "difficulty": types.Schema(type="INTEGER", description="Difficulty 1-5"),
                },
                required=["topic"],
            ),
        ),
        types.FunctionDeclaration(
            name="lookup_word",
            description=(
                "Look up the definition, pronunciation, and etymology of a word. "
                "Call this when: the student asks 'what does X mean?', encounters "
                "an unfamiliar term, or you detect confusion about terminology."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "word": types.Schema(type="STRING", description="The word to look up"),
                    "subject": types.Schema(type="STRING", description="The subject context"),
                },
                required=["word"],
            ),
        ),
        types.FunctionDeclaration(
            name="generate_visual",
            description=(
                "Generate a visual diagram/illustration to explain a concept. "
                "Call this when: the student says 'show me', 'draw', 'visualize', "
                "or when a concept is better explained with a picture."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "topic": types.Schema(type="STRING", description="What to visualize"),
                    "visual_type": types.Schema(
                        type="STRING",
                        description="Type: concept_map, flowchart, diagram, infographic",
                    ),
                },
                required=["topic"],
            ),
        ),
        types.FunctionDeclaration(
            name="create_bookmark",
            description=(
                "Save an important concept or definition for the student's revision. "
                "Call this when: you explain a key concept, define an important term, "
                "or the student says 'save this' or 'remember this'."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "text": types.Schema(type="STRING", description="The concept/definition to save"),
                    "tags": types.Schema(
                        type="ARRAY",
                        items=types.Schema(type="STRING"),
                        description="Tags like 'Biology', 'Key concept', 'Formula'",
                    ),
                },
                required=["text"],
            ),
        ),
        types.FunctionDeclaration(
            name="suggest_next_topic",
            description=(
                "Suggest what the student should study next based on their progress. "
                "Call this when the student asks 'what should I study next?' or "
                "finishes a topic."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "current_topic": types.Schema(type="STRING", description="What they just studied"),
                    "difficulty_so_far": types.Schema(type="INTEGER", description="How hard it was 1-5"),
                },
                required=["current_topic"],
            ),
        ),
        types.FunctionDeclaration(
            name="summarize_page",
            description=(
                "Create a concise bullet-point summary of the current textbook page. "
                "Call this when: the student says 'summarize this page', 'give me the key points', "
                "or seems overwhelmed by a dense page of text."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "page_text": types.Schema(type="STRING", description="The text content of the current page"),
                    "max_points": types.Schema(type="INTEGER", description="Maximum number of bullet points (3-8)"),
                },
                required=["page_text"],
            ),
        ),
        types.FunctionDeclaration(
            name="explain_like_im_5",
            description=(
                "Simplify a complex concept into an explanation a 5-year-old could understand. "
                "Uses analogies, everyday examples, and simple language. "
                "Call this when: the student says 'I still don't get it', 'make it simpler', "
                "or is clearly struggling after a first explanation."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "concept": types.Schema(type="STRING", description="The concept to simplify"),
                    "subject": types.Schema(type="STRING", description="The subject area"),
                },
                required=["concept"],
            ),
        ),
        types.FunctionDeclaration(
            name="compare_concepts",
            description=(
                "Create a side-by-side comparison of two concepts showing similarities and differences. "
                "Call this when: the student confuses two similar terms, asks 'what's the difference between X and Y', "
                "or is studying contrasting ideas."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "concept_a": types.Schema(type="STRING", description="First concept"),
                    "concept_b": types.Schema(type="STRING", description="Second concept"),
                    "subject": types.Schema(type="STRING", description="Subject context"),
                },
                required=["concept_a", "concept_b"],
            ),
        ),
        types.FunctionDeclaration(
            name="generate_flashcards",
            description=(
                "Generate study flashcards (front/back) from a topic for spaced repetition revision. "
                "Call this when: the student asks for flashcards, wants to prepare for revision, "
                "or finishes studying a chapter."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "topic": types.Schema(type="STRING", description="The topic to create flashcards for"),
                    "num_cards": types.Schema(type="INTEGER", description="Number of flashcards (3-10)"),
                },
                required=["topic"],
            ),
        ),
    ])
]


# ═══════════════════════════════════════════════
# Tool Execution — Backend runs the tool logic
# ═══════════════════════════════════════════════
async def execute_tool(name: str, args: dict, client) -> dict:
    """Execute a tool that Gemini autonomously decided to call."""

    if name == "generate_quiz":
        topic = args.get("topic", "General")
        num = min(args.get("num_questions", 3), 5)
        diff = args.get("difficulty", 3)
        
        quiz_type_arg = args.get("quiz_type", "multiple-choice").lower()
        if "fill" in quiz_type_arg:
            q_type_str = "fill-in-the-blanks"
        elif "true" in quiz_type_arg or "false" in quiz_type_arg:
            q_type_str = "true/false"
        else:
            q_type_str = "multiple-choice"

        response = client.models.generate_content(
            model=TEXT_MODEL,
            contents=[
                f"Generate {num} {q_type_str} questions about '{topic}' at difficulty {diff}/5. "
                f"Return JSON with 'questions' array. Each has: question (use _____ for fill in the blanks), options (4 choices always), correct_index, explanation."
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return {"quiz": json.loads(response.text), "tool": "generate_quiz"}

    elif name == "lookup_word":
        word = args.get("word", "")
        subject = args.get("subject", "General")

        response = client.models.generate_content(
            model=TEXT_MODEL,
            contents=[
                f'Word: "{word}"\n'
                f'Subject: {subject}\n'
                f'You are a dictionary and tutoring agent. Look up this word and return JSON with these exact keys:\n'
                f'- "ipa": IPA pronunciation string\n'
                f'- "pronunciation_guide": simple pronunciation guide for students\n'
                f'- "etymology": word origin/roots\n'
                f'- "general_definition": standard dictionary definition (string)\n'
                f'- "subject_definition": definition specific to {subject} context (string)\n'
                f'- "simple_analogy": explain to a 12-year-old using a relatable everyday analogy (string)\n'
                f'- "usage_in_context": usage example in context (string)\n'
                f'- "example_sentence": one clear example sentence using this word (string)\n'
                f'- "related_terms": list of 4 related terms from same subject (array of strings)\n'
                f'- "difficulty": how advanced this term is, 1-5 integer\n'
                f'- "fun_fact": one interesting/memorable fact about this concept (string)'
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                tools=[{"google_search": {}}],  # Grounded in real data
            ),
        )
        return {"definition": json.loads(response.text), "tool": "lookup_word"}

    elif name == "generate_visual":
        topic = args.get("topic", "")
        vtype = args.get("visual_type", "diagram")

        response = client.models.generate_content(
            model=IMAGE_MODEL,  # Nano Banana 2
            contents=[
                f"Create a clear, educational {vtype} about '{topic}'. "
                f"Style: clean, labeled, colorful, textbook-quality."
            ],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
        # Extract image if present
        result = {"tool": "generate_visual", "topic": topic}
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                result["image_b64"] = base64.b64encode(part.inline_data.data).decode()
                result["mime_type"] = part.inline_data.mime_type
            elif hasattr(part, 'text') and part.text:
                result["description"] = part.text
        return result

    elif name == "create_bookmark":
        return {
            "tool": "create_bookmark",
            "saved": True,
            "text": args.get("text", ""),
            "tags": args.get("tags", []),
        }

    elif name == "suggest_next_topic":
        current = args.get("current_topic", "")
        response = client.models.generate_content(
            model=TEXT_MODEL,
            contents=[
                f"Student just studied '{current}'. Suggest the 3 best next topics "
                f"in logical learning order. Return JSON: topics (array of strings), reason (string)."
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return {"suggestions": json.loads(response.text), "tool": "suggest_next_topic"}

    elif name == "summarize_page":
        page_text = args.get("page_text", "")
        max_points = min(args.get("max_points", 5), 8)

        response = client.models.generate_content(
            model=TEXT_MODEL,
            contents=[
                f"Summarize this page into {max_points} concise bullet points. "
                f"Focus on key concepts, definitions, and important facts.\n\nPage text:\n{page_text[:3000]}"
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return {"summary": json.loads(response.text), "tool": "summarize_page"}

    elif name == "explain_like_im_5":
        concept = args.get("concept", "")
        subject = args.get("subject", "General")

        response = client.models.generate_content(
            model=TEXT_MODEL,
            contents=[
                f'Explain "{concept}" ({subject}) like I\'m 5 years old. '
                f'Use a fun everyday analogy. Return JSON: simple_explanation, analogy, fun_fact.'
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return {"eli5": json.loads(response.text), "tool": "explain_like_im_5"}

    elif name == "compare_concepts":
        a = args.get("concept_a", "")
        b = args.get("concept_b", "")
        subject = args.get("subject", "General")

        response = client.models.generate_content(
            model=TEXT_MODEL,
            contents=[
                f'Compare "{a}" vs "{b}" in {subject}. Return JSON: '
                f'similarities (array of strings), differences (array of objects with a, b keys), '
                f'and a one_liner summary.'
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return {"comparison": json.loads(response.text), "tool": "compare_concepts"}

    elif name == "generate_flashcards":
        topic = args.get("topic", "")
        num = min(args.get("num_cards", 5), 10)

        response = client.models.generate_content(
            model=TEXT_MODEL,
            contents=[
                f"Create {num} study flashcards about '{topic}'. "
                f"Return JSON with 'cards' array. Each card has: front (question/term), "
                f"back (answer/definition), hint (optional clue)."
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return {"flashcards": json.loads(response.text), "tool": "generate_flashcards"}

    return {"error": f"Unknown tool: {name}"}


# ═══════════════════════════════════════════════
# WebSocket — Real-time voice + agentic loop
# ═══════════════════════════════════════════════
@router.websocket("/ws/live")
async def live_session(ws: WebSocket):
    """
    WebSocket bridge: Client ↔ Gemini Live API.
    The agent loop:
    1. Student speaks/types → sent to Gemini
    2. Gemini may respond with audio/text OR function_call
    3. If function_call → backend executes tool → sends result back to Gemini
    4. Gemini incorporates tool results → responds to student
    """
    await ws.accept()
    api_key = os.getenv("GEMINI_API_KEY", "")
    print(f"[LIVE] API key present: {bool(api_key)}, prefix: {api_key[:10]}..." if api_key else "[LIVE] WARNING: No API key found!")
    
    if not api_key:
        await ws.send_json({"type": "error", "message": "GEMINI_API_KEY not set on server"})
        await ws.close(code=1008, reason="API key not configured")
        return
    
    client = get_client()

    try:
        # Wait for config message from client
        init_data = await ws.receive_json()
        subject = init_data.get("subject", "General")
        grade = init_data.get("grade", "10")
        language = init_data.get("language", "English")
        voice = init_data.get("voice", "Kore")
        book_context = init_data.get("book_context", "")
        page_text = init_data.get("page_text", "")

        system_prompt = f"""You are Shivy AI, an expert {subject} tutor for Grade {grade} students.
You should default to speaking in {language}. 
However, if the student speaks a different language or explicitly asks you to change languages, you MUST switch to their requested language immediately and seamlessly.

Be conversational, use the student's name if they give it, and make learning fun!"""

        # Use the properly-defined AGENT_TOOLS (types.Tool objects)
        live_config = types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            system_instruction=types.Content(parts=[types.Part.from_text(text=system_prompt)]),
            tools=AGENT_TOOLS,
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)
                )
            ),
            input_audio_transcription=types.AudioTranscriptionConfig(),
            output_audio_transcription=types.AudioTranscriptionConfig(),
        )

        print(f"[LIVE] Connecting to Gemini model: {LIVE_MODEL} with voice={voice}...")
        async with client.aio.live.connect(
            model=LIVE_MODEL, config=live_config
        ) as session:
            print("[LIVE] Connected to Gemini Live API.")

            # Trigger immediate greeting and inject page text as context
            greeting_text = f"Hi there! Let's start our session."
            if page_text:
                greeting_text = f"[Page context: {page_text[:1000]}] {greeting_text}"
            await session.send_client_content(
                turns=[{"role": "user", "parts": [{"text": greeting_text}]}],
                turn_complete=True
            )
            print("[LIVE] Sent greeting trigger and context.")

            async def recv_from_gemini():
                """Listen for Gemini responses — audio, text, or tool calls.
                
                CRITICAL: session.receive() is PER-TURN. After a turn completes,
                the async generator exits. We must call it again in a loop to
                keep receiving responses across multiple conversation turns.
                (See official Gemini Live API audio example.)
                """
                try:
                    while True:
                        turn = session.receive()
                        async for response in turn:
                            try:
                                # Tool calls — agent behavior
                                if response.tool_call:
                                    function_responses = []
                                    for fc in response.tool_call.function_calls:
                                        # Execute the tool
                                        tool_result = await execute_tool(
                                            fc.name, dict(fc.args), client
                                        )

                                        # Notify frontend
                                        await ws.send_json({
                                            "type": "tool_call",
                                            "tool": fc.name,
                                            "args": dict(fc.args),
                                            "result": tool_result,
                                        })

                                        function_responses.append(
                                            types.FunctionResponse(
                                                id=fc.id,
                                                name=fc.name,
                                                response={"result": tool_result},
                                            )
                                        )

                                    # Send all tool results back to Gemini
                                    await session.send_tool_response(
                                        function_responses=function_responses
                                    )

                                # Audio data
                                if response.data is not None:
                                    header = bytes([0x01])
                                    await ws.send_bytes(header + response.data)

                                # Server content (text, turn complete, transcriptions)
                                if response.server_content:
                                    model_turn = response.server_content.model_turn
                                    if model_turn:
                                        for part in model_turn.parts:
                                            if hasattr(part, 'text') and part.text:
                                                await ws.send_json({
                                                    "type": "transcript",
                                                    "role": "ai",
                                                    "text": part.text,
                                                })
                                                print(f"[LIVE] Gemini Transcript (Part): {part.text}")

                                    # Output audio transcription (what the AI is saying in text)
                                    if hasattr(response.server_content, 'output_transcription') and response.server_content.output_transcription:
                                        text = response.server_content.output_transcription.text
                                        if text and text.strip():
                                            await ws.send_json({
                                                "type": "transcript",
                                                "role": "ai",
                                                "text": text,
                                            })

                                    # Input audio transcription (what the user is saying)
                                    if hasattr(response.server_content, 'input_transcription') and response.server_content.input_transcription:
                                        text = response.server_content.input_transcription.text
                                        if text and text.strip():
                                            await ws.send_json({
                                                "type": "transcript",
                                                "role": "user",
                                                "text": text,
                                            })
                                            print(f"[LIVE] Student Transcript: {text}")

                                    if response.server_content.turn_complete:
                                        await ws.send_json({"type": "turn_complete"})
                                        print("[LIVE] Gemini: Turn Complete")
                                    
                                    if response.server_content.interrupted:
                                        await ws.send_json({"type": "interrupted"})
                                        print("[LIVE] Gemini: Interrupted")

                            except Exception as resp_err:
                                # Log per-response errors but keep the loop alive
                                print(f"[LIVE] Error processing response: {type(resp_err).__name__}: {resp_err}")
                                try:
                                    await ws.send_json({"type": "error", "message": f"Response error: {resp_err}"})
                                except Exception:
                                    pass

                        print("[LIVE] Turn ended, waiting for next turn...")

                except asyncio.CancelledError:
                    print("[LIVE] Receiver task cancelled.")
                except Exception as e:
                    print(f"[LIVE] Receiver fatal error: {type(e).__name__}: {e}")
                    try:
                        await ws.send_json({"type": "error", "message": str(e)})
                    except Exception:
                        pass

            # Start receiving from Gemini in background
            print("[LIVE] Starting background receiver task...")
            recv_task = asyncio.create_task(recv_from_gemini())

            # Forward client messages to Gemini
            print("[LIVE] Entering bridge loop — waiting for student audio/text...")
            try:
                while True:
                    msg = await ws.receive()

                    if msg.get("type") == "websocket.disconnect":
                        break

                    try:
                        if "bytes" in msg:
                            raw = msg["bytes"]
                            msg_type = raw[0]
                            payload = raw[1:]

                            if msg_type == 0x00:
                                # Audio from mic (PCM 16kHz)
                                if not hasattr(ws, '_pcm_count'): ws._pcm_count = 0
                                ws._pcm_count += 1
                                if ws._pcm_count in (1, 10) or ws._pcm_count % 50 == 0:
                                    print(f"[LIVE] Forwarding audio to Gemini (chunk {ws._pcm_count}, {len(payload)} bytes)")
                                
                                await session.send_realtime_input(
                                    audio={"data": payload, "mime_type": "audio/pcm;rate=16000"}
                                )
                            elif msg_type == 0x10:
                                print(f"[LIVE] Forwarding video frame to Gemini ({len(payload)} bytes)")
                                await session.send_realtime_input(
                                    video={"data": payload, "mime_type": "image/jpeg"}
                                )

                        elif "text" in msg:
                            data = json.loads(msg["text"])

                            if data.get("type") == "text":
                                await session.send_client_content(
                                    turns=[{"role": "user", "parts": [{"text": data["content"]}]}],
                                    turn_complete=True
                                )
                            elif data.get("type") == "context_update":
                                await session.send_client_content(
                                    turns=[{"role": "user", "parts": [{"text": f"[Context update] Student is now on: {data.get('text', '')}"}]}],
                                    turn_complete=True
                                )
                            elif data.get("type") == "client_interruption":
                                # Explicitly halt the server's generation by sending an empty turn list
                                await session.send_client_content(turns=[], turn_complete=False)
                                # Echo the interruption signal back to the client to lock onto the new turn
                                await ws.send_json({"type": "interrupted"})

                    except Exception as bridge_err:
                        # Log per-message errors but keep the bridge loop alive
                        print(f"[LIVE] Bridge error: {type(bridge_err).__name__}: {bridge_err}")
                        continue

            except WebSocketDisconnect:
                pass
            finally:
                recv_task.cancel()

    except Exception as e:
        print(f"[LIVE] ERROR: {type(e).__name__}: {e}")
        try:
            await ws.send_json({"type": "error", "message": str(e)})
        except:
            pass
    finally:
        try:
            await ws.close()
        except:
            pass
