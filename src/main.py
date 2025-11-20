"""
Entry point for the Ebook Generator.
"""
import sys
from pathlib import Path

if __name__ == "__main__" and (__package__ is None or __package__ == ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    __package__ = "src"

from .pipeline import generate_ebook, save_ebook
from .ui import (
    print_completion_summary,
    print_info,
    print_separator,
    print_success_message,
    print_error_message
)

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ebook Generator")
    parser.add_argument("--test", action="store_true", help="Run in test mode (mocked LLM, fast execution)")
    args = parser.parse_args()

    try:
        # Gera ebook
        ebook = generate_ebook(test_mode=args.test)
        
        # Verifica se foi cancelado
        if ebook is None:
            exit(0)
        
        # Salva resultado
        print_info("Salvando ebook em Markdown...")
        output_path = save_ebook(ebook, test_mode=args.test)
        
        print_separator()
        
        # Exibe resumo final
        print_completion_summary(
            ebook['title'],
            len(ebook['chapters']),
            output_path
        )
        
        print_separator()
        print_success_message("Pipeline concluído com sucesso!")
        
    except KeyboardInterrupt:
        print_separator()
        print_error_message("Pipeline interrompido pelo usuário")
        exit(1)
    except Exception as e:
        print_separator()
        print_error_message(f"Erro durante execução: {str(e)}")
        exit(1)
