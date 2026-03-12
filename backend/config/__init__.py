"""
Centralized Model Configuration
=================================
Single source of truth for all Gemini model identifiers.
Change a model here → every router/service picks it up automatically.
"""

# ── Text / Reasoning ──────────────────────────────────────────────
# Fast, general-purpose model for text generation, quizzes, flashcards, etc.
TEXT_MODEL = "gemini-2.5-flash"

# ── Image Generation (Nano Banana 2) ─────────────────────────────
# High-fidelity image generation and editing
IMAGE_MODEL = "gemini-3.1-flash-image-preview"

# ── Live / Voice (Native Audio) ──────────────────────────────────
# Real-time bidirectional audio streaming for the voice tutor
LIVE_MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"

# ── Vision / Page Analysis ────────────────────────────────────────
# For analyzing uploaded textbook pages (images)
VISION_MODEL = "gemini-2.5-flash"

# ── Deep Research (if available) ──────────────────────────────────
DEEP_RESEARCH_MODEL = "gemini-2.5-pro"
