import os
import sys
from config_loader import EbookConfig

class EbookFactory:
    def __init__(self):
        self.config = EbookConfig()
        self.process_dir = "workspace/process"

    def get_status(self):
        checkpoints = sorted(glob.glob(f"{self.process_dir}/[0-9]*.md"))
        if not checkpoints:
            return "🌱 Fábrica pronta. Nenhum projeto em andamento."
        
        last_checkpoint = os.path.basename(checkpoints[-1])
        return f"🏭 Status: Projeto em andamento. Último checkpoint: {last_checkpoint}"

    def show_welcome(self):
        print("="*50)
        print("🚀 BEM-VINDO À TECHNICAL EBOOK FACTORY (KDP)")
        print("="*50)
        summary = self.config.get_summary()
        print(f"Capacidades: {len(summary['specs'])} Specs | {len(summary['author_styles'])} Estilos | {len(summary['author_visions'])} Visões")
        print("-"*50)
        print(self.get_status())
        print("-"*50)

if __name__ == "__main__":
    import glob # Needed for get_status
    factory = EbookFactory()
    factory.show_welcome()
