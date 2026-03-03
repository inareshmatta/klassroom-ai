"""
Tool Executor REST Endpoint
============================
When the client-side Gemini Live session issues a tool_call,
the frontend POSTs here to execute the tool on the server (keeping
the API key server-side) and sends the result back to Gemini.
"""
import json
import base64
from fastapi import APIRouter
from pydantic import BaseModel
from google.genai import types
from services.gemini_client import get_client

router = APIRouter(prefix="/api")


class ToolRequest(BaseModel):
    tool: str
    args: dict = {}


@router.post("/execute-tool")
async def execute_tool_endpoint(req: ToolRequest):
    """Execute a tool that Gemini autonomously decided to call."""
    client = get_client()
    result = await _execute(req.tool, req.args, client)
    return result


async def _execute(name: str, args: dict, client) -> dict:
    """Core tool execution logic — called by the REST endpoint."""

    if name == "generate_quiz":
        topic = args.get("topic", "General")
        num = min(args.get("num_questions", 3), 5)
        qtype = args.get("quiz_type", "mcq")
        diff = args.get("difficulty", 3)

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[
                f"Generate {num} {qtype} questions about '{topic}' at difficulty {diff}/5. "
                f"Return JSON with 'questions' array. Each has: question, options (4), correct_index, explanation."
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return {"quiz": json.loads(response.text), "tool": "generate_quiz"}

    elif name == "lookup_word":
        word = args.get("word", "")
        subject = args.get("subject", "General")

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[
                f'Define "{word}" for a {subject} student. Return JSON: '
                f'ipa, pronunciation_guide, etymology, subject_definition, simple_analogy, related_terms (4).'
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                tools=[{"google_search": {}}],
            ),
        )
        return {"definition": json.loads(response.text), "tool": "lookup_word"}

    elif name == "generate_visual":
        topic = args.get("topic", "")
        vtype = args.get("visual_type", "diagram")

        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[
                f"Create a clear, educational {vtype} about '{topic}'. "
                f"Style: clean, labeled, colorful, textbook-quality."
            ],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
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
            model="gemini-3-flash-preview",
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
            model="gemini-3-flash-preview",
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
            model="gemini-3-flash-preview",
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
            model="gemini-3-flash-preview",
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
            model="gemini-3-flash-preview",
            contents=[
                f"Create {num} study flashcards about '{topic}'. "
                f"Return JSON with 'cards' array. Each card has: front (question/term), "
                f"back (answer/definition), hint (optional clue)."
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return {"flashcards": json.loads(response.text), "tool": "generate_flashcards"}

    return {"error": f"Unknown tool: {name}"}
