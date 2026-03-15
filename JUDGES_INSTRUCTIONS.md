# 👨‍⚖️ Hackathon Judges' Instructions

This document provides a comprehensive, step-by-step guide for testing the advanced multimodal agentic capabilities of **Shivy AI**. 

> [!IMPORTANT]
> **JUDGE ACCESS KEY:** `GEMINI-LIVE-AGENT-26-MATTA`
> This key is required to start the Voice Tutor session.

---

## 🚀 Quick Access
- **Live Demo:** [https://shivy-ai-513107347048.us-central1.run.app/](https://shivy-ai-513107347048.us-central1.run.app/)
- **Architecture Diagram:** [README.md#system-architecture](./README.md#system-architecture)
- **Health Check:** [/health](https://shivy-ai-513107347048.us-central1.run.app/health)

---

## 🔍 Feature-by-Feature Testing Guide

Follow these steps to experience the full power of Shivy AI's agentic multimodal engine.

### Step 1: Initialize the Environment
1.  Open the [Live Demo](https://shivy-ai-513107347048.us-central1.run.app/).
2.  **Upload a PDF:** Drag and drop any textbook PDF into the left sidebar.
3.  **Wait for Analysis:** You will see a "Page Analysis Complete" system message in the right panel.

### Step 2: Interactive Word & Phrase Tools
1.  **Dictionary Lookup:** Click any single word on the PDF canvas. A tooltip will slide out showing phonetic pronunciation, etymology, and subject-specific definitions.
2.  **Phrase Selection:** Highlight a sentence or phrase. The same tooltip will appear, analyzing the selected context.
3.  **Knowledge Vault:** Click the **🔖 Save** icon in the tooltip. Verify the word appears in the **Knowledge Vault** (bottom right).
4.  **Instant Visualization:** Click the **🎨 Visualize** icon in the tooltip. The Visual Explainer will open with the concept pre-loaded.

### Step 3: Voice Tutor & Security 🎙️
1.  Locate the **"Judge Access Key"** input above the Start button.
2.  Enter: `GEMINI-LIVE-AGENT-26-MATTA`
3.  Click **🎙 Start Tutor**. 
4.  **The Greeting:** The AI will introduce itself and confirm it can see your PDF.
5.  **Barge-in Test:** While the AI is speaking, interrupt it by saying *"Wait, can you explain that differently?"*. 
    - *Expected behavior: AI stops audio immediately and responds to your interruption.*

### Step 4: Continuous Vision & Discipline 📹
1.  Start a voice session.
2.  **Test 1 (Normal):** Look down at a book or write on a paper. AI should remain silent (trained to recognize studying).
3.  **Test 2 (Nudge):** Cover your webcam completely with your hand.
    - *Expected behavior: Within 10-15 seconds, the AI will verbally nudge you: "I can't see you, are you still there?" and a "Camera Off" log will appear in the Session Activity panel.*

### Step 5: Guided Reading & Proactive Tutoring 📖
1.  With a session active, say *"Read this page to me"*.
2.  Observe the AI reading a paragraph with human-like prosody.
3.  **The Agentic Pause:** After the paragraph, it will pause and ask: *"Should we do a quick quiz, or do you need help with a word?"*
4.  Say *"Quiz me"*. 
    - *Expected behavior: The Assessment Panel slides open automatically with questions from that exact paragraph.*

### Step 6: Interactive Dictation Homework 📝
1.  While in a session, say *"Let's do some dictation"*.
2.  AI asks: *"2, 3, or 5 words?"*. Answer *"2"*.
3.  Follow the flow: AI dictates a word -> You say *"Next"* -> AI dictates the next word.
4.  **Vision Verification:** Hold up a paper with the words written down to your webcam.
    - *Expected behavior: AI uses Vision to read your handwriting, provides verbal corrections, and only THEN saves the words to the Session Activity logs.*

### Step 7: Visual Explainer (Concept Mapping) 🎨
1.  Either click a word -> Visualize OR ask the tutor: *"Can you draw the Krebs Cycle for me?"*
2.  Watch the **Visual Explainer** panel slide open.
3.  Click **"Generate Diagram"**. observe the technical concept map appear, grounded in web search data.

### Step 8: Image Homework Review 👁️
1.  Click **"Add book"** in the sidebar.
2.  Upload a `.jpg` or `.png` of handwritten math or text.
3.  Click the **👁️ Review Homework** button in the top bar.
4.  *Expected behavior: The AI analyzes the uploaded image using Gemini Vision and provides a spoken critique of the solutions/handwriting.*

---

## 🛠️ Technical Highlights for Judges
- **Direct-to-TPU Pipeline:** Audio streams directly from the browser to Google's Native Audio API via WebSockets.
- **Ephemeral Credentials:** The backend mints 60-second single-use tokens to protect the Gemini API key from client-side exposure.
- **VAD Orchestration:** Uses server-side Voice Activity Detection to handle barge-ins and interruptions instantly.
- **TextLayer DOM Sync:** Every word in the PDF is mapped to an invisible DOM layer for pixel-perfect interactivity.

---
Built with ❤️ by the Shivy AI Team.
