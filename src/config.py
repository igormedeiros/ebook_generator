"""
Configuration module for Ebook Generator.
Handles environment setup and model initialization.
Supports dual-model strategy: Gemini 2.5 Flash (writing) and Gemini 2.5 Pro (research).
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_model() -> ChatGoogleGenerativeAI:
    """
    Initialize and return the writing model (Gemini 2.5 Flash).
    Uses Gemini 2.5 Flash for fast, creative text generation and iterative refinement.
    
    Configuration:
    - Model: gemini-2.5-flash
    - Temperature: 0.7 (balanced creativity and consistency)
    - top_p: 0.95
    - top_k: 40
    
    Used for: Writing, revision, creativity-focused tasks
    
    Returns:
        ChatGoogleGenerativeAI: Configured Gemini 2.5 Flash model
    
    Raises:
        ValueError: If GOOGLE_API_KEY environment variable not set
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.7,  # Balanced creativity and consistency
        top_p=0.95,
        top_k=40,
    )


def get_research_model() -> ChatGoogleGenerativeAI:
    """
    Initialize and return the research model (Gemini 2.5 Pro).
    Uses Gemini 2.5 Pro for deep analysis, RAG retrieval, and semantic search.
    
    Configuration:
    - Model: gemini-2.5
    - Temperature: 0.3 (focused on precision and factuality)
    - top_p: 0.95
    - top_k: 40
    
    Used for: Research, RAG integration, fact-checking, semantic analysis
    
    Returns:
        ChatGoogleGenerativeAI: Configured Gemini 2.5 Pro model
    
    Raises:
        ValueError: If GOOGLE_API_KEY environment variable not set
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.5",
        google_api_key=api_key,
        temperature=0.3,  # Focused on precision and factuality for RAG
        top_p=0.95,
        top_k=40,
    )
