# 🧑‍⚖️ Klassbook AI - Judge Testing Instructions

Welcome! To evaluate **Klassbook AI**, please follow these steps to bypass the public landing page restriction and test all the interactive multimodal features.

## 🔑 Accessing the App

1. Go to the live application: **[https://klassbook-ai-kygarr5jkq-uc.a.run.app](https://klassbook-ai-kygarr5jkq-uc.a.run.app)**
2. In the "Enter Judge Access Code" input box, type: **`Gemini-Live-Agent-26-MATTA`**
3. Click **Start Learning** to enter the main classroom interface.

---

## 🧪 Reproducible Testing Instructions

Once inside the app, here is how you can test every interactive feature:

### Test 1: Upload a PDF & Interactive Words
1. Drag any PDF document into the upload area on the left panel.
2. **Click any word** on the rendered page → a dictionary tooltip appears with pronunciation, etymology, and contextual definition.
3. Click **🔖 Save** → the word appears in your **Knowledge Vault** (right panel).
4. **Highlight a multi-word phrase** → the same smart tooltip generates for the entire selection.

### Test 2: Voice Tutor (Real-time Conversation)
1. With a PDF loaded, click **🎙 Start Tutor** in the top-left panel.
2. Allow microphone access when prompted.
3. **Speak normally**: *"Can you explain what's on this page?"*
4. The AI should respond **within 1-2 seconds** with spoken audio.
5. **Test barge-in**: While the AI is speaking, interrupt it by saying *"Wait, what does that mean?"* — the AI will instantly stop talking and respond to your interruption.

### Test 3: Autonomous AI Tools & Visuals
1. While talking to the Voice Tutor, say: *"I don't understand this. Can you generate a visual diagram for me?"*
2. The AI will autonomously decide to trigger the `generate_visual` tool.
3. The **Visual Canvas** panel will *automatically* slide open, displaying the generated infographic, flow chart, or concept map.
4. Now, ask the tutor to test you: *"Can you give me a quiz on this topic?"*
5. The AI will trigger the `generate_quiz` tool.
6. The **Assessment Center** will *automatically* open with a generated quiz (MCQs, True/False, Fill in the blanks) ready to be taken.

### Test 4: Explain Page & Diagrams (Vision)
1. Navigate to a page with complex diagrams, schemas, or charts in the PDF.
2. Click the **👁️ Explain Page & Diagrams** button above the PDF canvas.
3. The app captures a pixel-perfect image of the canvas and uses Gemini Vision to verbally describe the specific visual content you are looking at.

### Test 5: Predictive Curriculum Planner
1. Click **📅 Study Planner** in the top navigation or left panel.
2. Set an exam date and daily study hours → click **Generate Plan**.
3. A personalized, week-by-week study schedule appears based on the book's contents. You can check off tasks to track your progress.

---

Thank you for reviewing **Klassbook AI**! Let us know if you run into any issues.
