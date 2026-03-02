"""Test with the EXACT same config as live_session.py uses"""
import asyncio
import os
import json
from dotenv import load_dotenv
load_dotenv(r"d:\KlassroomAI\backend\.env")

from google import genai
from google.genai import types

async def test():
    api_key = os.getenv("GEMINI_API_KEY", "")
    print(f"Key: {api_key[:15]}...")
    client = genai.Client(api_key=api_key)
    
    # Recreate EXACTLY the same config as live_session.py
    system_prompt = "You are KlassroomAI, an expert tutor. Be friendly and helpful."
    
    # Simple tool declaration
    tools = [{
        "function_declarations": [{
            "name": "generate_quiz",
            "description": "Generate a quiz",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                },
                "required": ["topic"]
            }
        }]
    }]
    
    live_config = {
        "response_modalities": ["AUDIO"],
        "system_instruction": system_prompt,
        "tools": tools,
    }
    
    print(f"\nConnecting with config: modalities=AUDIO, tools=1, system_prompt={len(system_prompt)} chars")
    
    try:
        async with client.aio.live.connect(
            model="gemini-2.5-flash-native-audio-preview-12-2025",
            config=live_config
        ) as session:
            print("CONNECTED! Sending test message...")
            await session.send_client_content(
                turns={"parts": [{"text": "Hello, say hi back briefly"}]}
            )
            async for resp in session.receive():
                if resp.text:
                    print(f"Got text: {resp.text}")
                    break
                if resp.data:
                    print(f"Got audio data: {len(resp.data)} bytes")
                    break
            print("SUCCESS!")
    except Exception as e:
        print(f"FAILED: {type(e).__name__}: {e}")

asyncio.run(test())
