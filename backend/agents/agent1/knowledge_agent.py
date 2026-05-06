"""
Interview Ace — Knowledge Agent (Agent 1)

Responsibilities:
1. Ingest job descriptions, resumes, and reference materials
2. Build and maintain a RAG index over ingested documents
3. Given a transcribed question from the interviewer, generate a smart answer
4. Support multiple LLM backends (OpenAI, Anthropic, Google, DeepSeek)

Pipeline:
    Question (from Voice Agent)
        → RAG retrieval (find relevant context from knowledge base)
        → LLM prompt assembly (system prompt + context + question)
        → Answer generation
        → Return to frontend

Usage:
    agent = KnowledgeAgent(llm_provider="openai", model="gpt-4o")
    answer = await agent.generate_answer("What is your experience with Kubernetes?")
"""

from loguru import logger


class KnowledgeAgent:
    """Generates contextual answers using RAG + LLM."""

    def __init__(self, llm_provider: str = "openai", model: str = "gpt-4o", api_key: str = ""):
        self.llm_provider = llm_provider
        self.model = model
        self.api_key = api_key
        self._client = None

    async def initialize(self):
        """Initialize LLM client and load knowledge base."""
        # TODO: Create LLM client based on provider
        # if self.llm_provider == "openai":
        #     self._client = AsyncOpenAI(api_key=self.api_key)
        # elif self.llm_provider == "anthropic":
        #     self._client = AsyncAnthropic(api_key=self.api_key)
        logger.info(f"🧠 Knowledge Agent initialized (provider={self.llm_provider}, model={self.model})")

    async def generate_answer(self, question: str, context: list[str] = None) -> dict:
        """Generate an answer for the given interview question.

        Args:
            question: Transcribed question from the interviewer
            context: Optional pre-retrieved context chunks from RAG

        Returns:
            dict with keys: answer, confidence, sources
        """
        # Step 1: Retrieve relevant context via RAG (if not provided)
        if context is None:
            context = await self._retrieve_context(question)

        # Step 2: Assemble prompt
        system_prompt = self._build_system_prompt(context)

        # Step 3: Call LLM
        # response = await self._client.chat.completions.create(
        #     model=self.model,
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": question},
        #     ],
        #     temperature=0.3,
        #     max_tokens=500,
        # )

        # TODO: Return structured response
        return {
            "answer": f"[TODO] Answer to: {question}",
            "confidence": 0.0,
            "sources": [],
        }

    async def _retrieve_context(self, query: str, top_k: int = 5) -> list[str]:
        """Retrieve relevant document chunks from the RAG index."""
        # TODO: Query vector DB
        return []

    def _build_system_prompt(self, context: list[str]) -> str:
        """Build the system prompt with retrieved context."""
        context_text = "\n---\n".join(context) if context else "No relevant context found."
        return f"""You are an AI interview assistant. Your job is to help the candidate answer interview questions.

RULES:
1. Generate concise, professional answers based on the candidate's actual experience
2. Use the provided context (resume, job description, notes) to personalize answers
3. Be honest — do not fabricate experience the candidate doesn't have
4. Keep answers under 2 minutes when spoken aloud (~300 words)
5. Structure answers using STAR method when applicable (Situation, Task, Action, Result)

CANDIDATE CONTEXT:
{context_text}
"""
