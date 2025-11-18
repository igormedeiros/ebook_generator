"""
LLM Fallback Strategy - Multi-model orchestration with automatic failover.

Implements intelligent fallback mechanism:
1. Gemini 2.5 Pro (research, high accuracy, low quota)
2. Gemini 2.5 Flash (writing, creative, higher quota)
3. Groq LLaMA 3 70B (fallback, unlimited free tier)

Each tier is tried in sequence until one succeeds.
"""

import os
from typing import Any, Callable, Dict, List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from .config import get_logger

logger = get_logger(__name__)


class LLMFallback:
    """Multi-model LLM orchestrator with automatic failover."""
    
    def __init__(self):
        """Initialize LLM models in fallback order."""
        self.models = []
        self.setup_models()
        # Precompute sequences for different workloads
        self._research_sequence = [self.models[0], self.models[1], self.models[2]]
        self._write_sequence = [self.models[1], self.models[0], self.models[2]]

    def _describe_model(self, model: Any) -> str:
        """Return readable name for logging."""

        return getattr(model, "model", getattr(model, "model_name", type(model).__name__))

    def _extract_response(self, response: Any) -> str:
        """Normalize different agent response structures into a string."""

        if isinstance(response, dict):
            if "output" in response:
                return response["output"]
            if "messages" in response:
                messages = response.get("messages", [])
                if messages:
                    return messages[-1].content
        return str(response)

    def _get_sequence(self, mode: str) -> List[Dict[str, Any]]:
        """Return ordered list of models for the requested workload."""

        if mode == "research":
            return list(self._research_sequence)
        if mode == "write":
            return list(self._write_sequence)
        return list(self.models)

    @staticmethod
    def _replace_agent_model(agent: Any, model: Any) -> bool:
        """Attempt to swap the underlying LLM used by the agent in-place."""

        # AgentExecutor exposes .agent.llm_chain.llm and .llm_chain.llm
        swapped = False
        chain_candidates = []
        if hasattr(agent, "agent") and hasattr(agent.agent, "llm_chain"):
            chain_candidates.append(agent.agent.llm_chain)
        if hasattr(agent, "llm_chain"):
            chain_candidates.append(agent.llm_chain)

        for chain in chain_candidates:
            if hasattr(chain, "llm"):
                chain.llm = model
                swapped = True

        return swapped
    
    def setup_models(self):
        """Setup LLM models in priority order."""
        # Priority 1: Gemini 2.5 Pro (high accuracy)
        self.models.append({
            "name": "Gemini 2.5 Pro",
            "model_id": "gemini-2.5-pro",
            "init": self._init_gemini_pro,
            "description": "Google Gemini 2.5 Pro (Research mode)"
        })
        
        # Priority 2: Gemini 2.5 Flash (good accuracy, higher quota)
        self.models.append({
            "name": "Gemini 2.5 Flash",
            "model_id": "gemini-2.5-flash",
            "init": self._init_gemini_flash,
            "description": "Google Gemini 2.5 Flash (Writing mode)"
        })
        
        # Priority 3: Groq LLaMA 3 70B (unlimited free tier)
        self.models.append({
            "name": "Groq LLaMA 3 70B",
            "model_id": "llama-3.3-70b-versatile",
            "init": self._init_groq,
            "description": "Groq LLaMA 3 70B (Fallback, unlimited free tier)"
        })
    
    @staticmethod
    def _init_gemini_pro() -> ChatGoogleGenerativeAI:
        """Initialize Gemini 2.5 Pro model."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key=api_key,
            temperature=0.3,
            top_p=0.95,
            top_k=40,
        )
    
    @staticmethod
    def _init_gemini_flash() -> ChatGoogleGenerativeAI:
        """Initialize Gemini 2.5 Flash model."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7,
            top_p=0.95,
            top_k=40,
        )
    
    @staticmethod
    def _init_groq() -> ChatGroq:
        """Initialize Groq LLaMA 3 70B model."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=api_key,
            temperature=0.7,
            max_tokens=2048,
        )
    
    def get_research_model(self) -> Any:
        """
        Get research model with fallback.
        
        Try Gemini Pro first (high accuracy), then flash, then Groq.
        
        Returns:
            ChatGoogleGenerativeAI or ChatGroq: First available model
            
        Raises:
            RuntimeError: If no models are available
        """
        logger.info("🔄 Inicializando modelo de pesquisa com fallback...")
        
        for model_config in self.models:
            try:
                logger.info(f"  📊 Tentando: {model_config['description']}")
                model = model_config["init"]()
                logger.info(f"  ✅ Sucesso: {model_config['name']}")
                return model
            except Exception as e:
                logger.warning(f"  ⚠️  Falhou {model_config['name']}: {str(e)[:100]}")
                continue
        
        raise RuntimeError("❌ Nenhum modelo LLM disponível!")
    
    def get_write_model(self) -> Any:
        """
        Get writing model with fallback.
        
        Try Gemini Flash first (faster, creative), then Pro, then Groq.
        
        Returns:
            ChatGoogleGenerativeAI or ChatGroq: First available model
            
        Raises:
            RuntimeError: If no models are available
        """
        logger.info("🔄 Inicializando modelo de escrita com fallback...")
        
        # For writing, prefer Flash (faster) -> Pro (accurate) -> Groq (fallback)
        write_priority = [
            self.models[1],  # Flash
            self.models[0],  # Pro
            self.models[2],  # Groq
        ]
        
        for model_config in write_priority:
            try:
                logger.info(f"  📝 Tentando: {model_config['description']}")
                model = model_config["init"]()
                logger.info(f"  ✅ Sucesso: {model_config['name']}")
                return model
            except Exception as e:
                logger.warning(f"  ⚠️  Falhou {model_config['name']}: {str(e)[:100]}")
                continue
        
        raise RuntimeError("❌ Nenhum modelo LLM disponível!")
    
    def execute_with_fallback(
        self,
        query: str,
        agent: Any,
        agent_factory: Optional[Callable[[Any], Any]] = None,
        mode: str = "write",
        skip_model_id: Optional[str] = None,
    ) -> str:
        """Execute agent with automatic fallback on failure."""

        sequence = self._get_sequence(mode)
        total_candidates = len(sequence)
        if skip_model_id:
            sequence = [cfg for cfg in sequence if cfg.get("model_id") != skip_model_id]

        if not sequence:
            raise RuntimeError("❌ Sem modelos alternativos disponíveis para fallback")

        logger.info(
            f"🔄 Executando fallback ({len(sequence)}/{total_candidates} modelos elegíveis)..."
        )
        last_error: Optional[Exception] = None

        for idx, model_config in enumerate(sequence, 1):
            try:
                logger.info(f"\n[Tentativa {idx}/{len(sequence)}] 📊 {model_config['name']}")
                logger.info(f"   {model_config['description']}")

                model = model_config["init"]()
                logger.info(
                    f"   ⏳ Processando com {model_config['name']} ({self._describe_model(model)})..."
                )

                current_agent = None
                if agent_factory:
                    current_agent = agent_factory(model)
                else:
                    swapped = self._replace_agent_model(agent, model)
                    if swapped:
                        current_agent = agent
                    else:
                        raise RuntimeError(
                            "Agent does not expose llm_chain; provide agent_factory for fallback."
                        )

                setattr(current_agent, "_fallback_model_id", model_config.get("model_id"))
                response = current_agent.invoke({
                    "messages": [{"role": "user", "content": query}]
                })
                result = self._extract_response(response)
                logger.info(f"   ✅ Sucesso com {model_config['name']}")
                return result

            except Exception as error:  # noqa: BLE001
                last_error = error
                error_msg = str(error)
                logger.warning(f"   ❌ Falhou {model_config['name']}: {error_msg[:120]}")
                if "ResourceExhausted" in str(type(error)) or "429" in error_msg:
                    logger.warning("   💬 Quota excedida - tentando próximo modelo...")

        raise RuntimeError(
            f"❌ Todos os modelos de fallback falharam ({len(sequence)} tentativas)! "
            f"Último erro: {last_error}"
        )


# Global instance
_llm_fallback = None


def get_llm_fallback() -> LLMFallback:
    """Get or create global LLM fallback orchestrator."""
    global _llm_fallback
    if _llm_fallback is None:
        _llm_fallback = LLMFallback()
    return _llm_fallback


def get_research_model_with_fallback() -> Any:
    """Get research model with automatic fallback."""
    return get_llm_fallback().get_research_model()


def get_write_model_with_fallback() -> Any:
    """Get write model with automatic fallback."""
    return get_llm_fallback().get_write_model()
