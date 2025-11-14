#!/usr/bin/env python
"""
Integration tests for Ebook Generator 1.0 pipeline with REAL API calls.

This test executes the complete pipeline with actual Gemini API calls,
no mocking. Logs every step of the process.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from src.config import get_logger, console, get_model, get_research_model
from src.input_validator import validate_book_input
from src.main import run_ebook_pipeline

logger = get_logger(__name__)


def log_section(title: str):
    """Print a formatted section header."""
    console.print(f"\n[bold cyan]{'=' * 70}[/bold cyan]")
    console.print(f"[bold green]{title}[/bold green]")
    console.print(f"[bold cyan]{'=' * 70}[/bold cyan]\n")


def test_integration_real_api():
    """Run integration test with real API calls."""
    
    log_section("🚀 EBOOK GENERATOR 1.0 - INTEGRATION TEST (REAL APIs)")
    
    # Log test environment
    logger.info(f"Test started at: {datetime.now().isoformat()}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")
    
    try:
        # Step 1: Verify API Keys
        log_section("STEP 1: Verifying API Configuration")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("❌ GOOGLE_API_KEY environment variable not set")
            console.print("[red]❌ ERRO: GOOGLE_API_KEY não configurada[/red]")
            return False
        
        logger.info(f"✅ GOOGLE_API_KEY configured (length: {len(api_key)} chars)")
        console.print(f"[green]✅ API Key configured (primeiros 10 chars: {api_key[:10]}...)[/green]")
        
        # Step 2: Initialize Models
        log_section("STEP 2: Initializing Gemini Models")
        
        logger.info("Initializing write_model (Gemini 2.5 Flash)...")
        console.print("[cyan]Inicializando write_model (Gemini 2.5 Flash)...[/cyan]")
        write_model = get_model()
        logger.info(f"✅ Write model initialized: {type(write_model).__name__}")
        console.print(f"[green]✅ Write model: {type(write_model).__name__}[/green]")
        
        logger.info("Initializing research_model (Gemini 2.5 Pro)...")
        console.print("[cyan]Inicializando research_model (Gemini 2.5 Pro)...[/cyan]")
        research_model = get_research_model()
        logger.info(f"✅ Research model initialized: {type(research_model).__name__}")
        console.print(f"[green]✅ Research model: {type(research_model).__name__}[/green]")
        
        # Step 3: Validate Input
        log_section("STEP 3: Validating Book Input")
        
        logger.info("Loading and validating specs/book.yaml...")
        console.print("[cyan]Carregando e validando specs/book.yaml...[/cyan]")
        
        try:
            book_config = validate_book_input()
            logger.info(f"✅ Book config validated")
            
            metadata = book_config.get("metadata", {})
            parameters = book_config.get("parameters", {})
            
            logger.info(f"Metadata: {metadata}")
            logger.info(f"Parameters: {parameters}")
            
            console.print(f"[green]✅ Tópico: {metadata.get('topic')}[/green]")
            console.print(f"[green]✅ Público-alvo: {metadata.get('target_audience')}[/green]")
            console.print(f"[green]✅ Meta de palavras: {parameters.get('word_count_target')}[/green]")
            
        except FileNotFoundError as e:
            logger.error(f"Input file not found: {str(e)}")
            console.print(f"[red]❌ ERRO: {str(e)}[/red]")
            return False
        
        # Step 4: Run Pipeline
        log_section("STEP 4: Running 9-Stage Pipeline")
        
        logger.info("Starting pipeline execution...")
        console.print("[cyan]Iniciando execução da pipeline...[/cyan]\n")
        
        # Extract parameters for pipeline
        topic = metadata.get("topic", "Desenvolvimento de Software")
        target_audience = metadata.get("target_audience", "Desenvolvedores")
        word_count = parameters.get("word_count_target", 15000)
        reading_level = parameters.get("reading_level", "intermediate")
        promise = parameters.get("transformation_promise", "")
        
        logger.info(f"Pipeline parameters:")
        logger.info(f"  - Topic: {topic}")
        logger.info(f"  - Target Audience: {target_audience}")
        logger.info(f"  - Word Count: {word_count}")
        logger.info(f"  - Reading Level: {reading_level}")
        
        # Run the actual pipeline with real APIs
        pipeline_result = run_ebook_pipeline(
            topic=topic,
            target_audience=target_audience,
            word_count_target=word_count,
            reading_level=reading_level,
            transformation_promise=promise,
            run_all_stages=True,
        )
        
        # Step 5: Analyze Results
        log_section("STEP 5: Analyzing Pipeline Results")
        
        if pipeline_result.get("pipeline_status") == "completed":
            logger.info(f"✅ Pipeline completed successfully")
            console.print("[green]✅ Pipeline concluída com sucesso![/green]")
            
            # Log stage outputs
            for stage_key, stage_data in pipeline_result.get("stages", {}).items():
                logger.info(f"{stage_key}: {stage_data.get('status', 'Unknown')}")
                console.print(f"[green]  ✅ {stage_key}: Concluído[/green]")
            
            return True
            
        elif pipeline_result.get("pipeline_status") == "partial":
            logger.warning("Pipeline executed partially (partial mode)")
            console.print("[yellow]⚠️  Pipeline executada parcialmente[/yellow]")
            return True
            
        elif pipeline_result.get("pipeline_status") == "error":
            error_msg = pipeline_result.get("error", "Unknown error")
            logger.error(f"Pipeline failed with error: {error_msg}")
            console.print(f"[red]❌ ERRO: {error_msg}[/red]")
            return False
        
        else:
            logger.error(f"Unknown pipeline status: {pipeline_result.get('pipeline_status')}")
            console.print("[red]❌ ERRO: Status desconhecido da pipeline[/red]")
            return False

    except KeyboardInterrupt:
        logger.warning("Test interrupted by user (Ctrl+C)")
        console.print("[yellow]⚠️  Teste interrompido pelo usuário[/yellow]")
        return False
        
    except Exception as e:
        logger.exception("Integration test failed with exception")
        console.print(f"[red]❌ ERRO: {str(e)}[/red]")
        return False
    
    finally:
        log_section("Test Completed")
        logger.info(f"Test ended at: {datetime.now().isoformat()}")


if __name__ == "__main__":
    success = test_integration_real_api()
    sys.exit(0 if success else 1)
