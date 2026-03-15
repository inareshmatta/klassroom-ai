# 👨‍💻 Project Contribution: [Your Name] (Solo Developer)

I served as the sole developer, architect, and designer for **Shivy AI**, responsible for the end-to-end execution of the project—from conceptual pedagogical design to full-stack deployment.

## Key Technical Contributions

- **Multimodal Architecture**: Designed and implemented a high-performance, direct client-to-server pipeline using the **Gemini Live API** (@google/genai SDK). This involved architecting a raw PCM audio stream and a continuous vision pre-processor to enable zero-latency, "barge-in" interactions.
- **Agentic Orchestration**: Built a custom decision-engine that allows the AI to autonomously trigger educational tools (MCQ quizzes, visual generation, etymology lookups) based on the student's real-time needs and behavior.
- **Vision Suite Optimization**: Engineered a canvas-based image pre-processor that force-resizes and compresses webcam frames to sub-20KB payloads. This was critical for maintaining WebSocket stability and crystal-clear audio during vision-heavy tasks like handwriting verification.
- **Full-Stack Implementation**: Developed a scalable backend using **FastAPI** on **Google Cloud Run**, integrated with **Google Secret Manager** for secure key management and an ephemeral token protocol for safe client-side authentication.
- **Educational UX Design**: Designed a student-focused interface that bridges digital PDF content with physical handwriting, ensuring the "Vision-Verified Dictation" feature felt natural and encouraging for learners.
- **Infrastructure & DevOps**: Managed the entire deployment stack, including the creation of Docker containers and the implementation of a one-click CI/CD pipeline on Google Cloud.

This project allowed me to push the boundaries of current AI capabilities, moving from a standard chatbot model to a truly agentic, multimodal tutor that sees, hears, and responds to students in real-time.
