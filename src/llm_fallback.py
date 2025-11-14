"""
LLM Fallback Strategy - Multi-model orchestration with automatic failover.

Implements intelligent fallback mechanism:
1. Gemini 2.5 Pro (research, high accuracy, low quota)
2. Gemini 2.5 Flash (writing, creative, higher quota)
3. Groq LLaMA 3 70B (fallback, unlimited free tier)

Each tier is tried in sequence until one succeeds.
"""

import os
from typing import Optional, Any, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from src.config import get_logger

logger = get_logger(__name__)


class LLMFallback:
    """Multi-model LLM orchestrator with automatic failover."""
    
    def __init__(self):
        """Initialize LLM models in fallback order."""
        self.models = []
        self.setup_models()
    
    def setup_models(self):
        """Setup LLM models in priority order."""
        # Priority 1: Gemini 2.5 Pro (high accuracy, low quota)
        self.models.append({
            "name": "Gemini 2.5 Pro",
            "init": self._init_gemini_pro,
            "description": "Google Gemini 2.5 Pro (Research mode, 2 req/min free tier)"
        })
        
        # Priority 2: Gemini 2.5 Flash (good accuracy, higher quota)
        self.models.append({
            "name": "Gemini 2.5 Flash",
            "init": self._init_gemini_flash,
            "description": "Google Gemini 2.5 Flash (Writing mode, 15 req/min free tier)"
        })
        
        # Priority 3: Groq LLaMA 3 70B (unlimited free tier)
        self.models.append({
            "name": "Groq LLaMA 3 70B",
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
        agent: Any,
        query: str,
        model_sequence: Optional[list] = None
    ) -> str:
        """
        Execute agent with automatic fallback on failure.
        
        Args:
            agent: LangChain agent to execute
            query: Query string for agent
            model_sequence: Optional list of models to try (default: all)
        
        Returns:
            str: Agent response
            
        Raises:
            RuntimeError: If all models fail
        """
        logger.info(f"🔄 Executando com fallback ({len(self.models)} modelos disponíveis)...")
        
        for idx, model_config in enumerate(self.models, 1):
            try:
                logger.info(f"\n[Tentativa {idx}/{len(self.models)}] 📊 {model_config['name']}")
                logger.info(f"   {model_config['description']}")
                
                # Try to get and use the model
                model = model_config["init"]()
                
                # Execute agent with this model
                logger.info(f"   ⏳ Processando com {model_config['name']}...")
                response = agent.invoke({
                    "messages": [{"role": "user", "content": query}]
                })
                
                # Extract response
                if isinstance(response, dict):
                    if "output" in response:
                        result = response["output"]
                    elif "messages" in response:
                        messages = response.get("messages", [])
                        result = messages[-1].content if messages else str(response)
                    else:
                        result = str(response)
                else:
                    result = str(response)
                
                logger.info(f"   ✅ Sucesso com {model_config['name']}")
                return result
                
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"   ❌ Falhou {model_config['name']}: {error_msg[:80]}")
                
                # Log specific quota errors
                if "ResourceExhausted" in str(type(e)) or "429" in error_msg:
                    logger.warning(f"   💬 Quota excedida - tentando próximo modelo...")
                
                continue
        
        raise RuntimeError(
            f"❌ Todos os {len(self.models)} modelos falharam! "
            "Verifique suas credenciais de API."
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
