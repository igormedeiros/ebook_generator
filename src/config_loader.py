import os
import glob

class EbookConfig:
    def __init__(self):
        self.factory = {}
        self.types = {}
        self.author = {
            "bio": "",
            "stories": "",
            "styles": {},
            "visions": {}
        }
        self.load_all()

    def load_all(self):
        # Load Factory Rules (Global Specs)
        for filepath in glob.glob("ebook/factory/*.md"):
            name = os.path.basename(filepath).replace(".md", "").lower()
            with open(filepath, 'r', encoding='utf-8') as f:
                self.factory[name] = f.read()

        # Load Book Types
        for filepath in glob.glob("ebook/types/*.md"):
            name = os.path.basename(filepath).replace(".md", "").lower()
            with open(filepath, 'r', encoding='utf-8') as f:
                self.types[name] = f.read()

        # Load Author Master Data
        if os.path.exists("ebook/author/BIO.md"):
            with open("ebook/author/BIO.md", 'r', encoding='utf-8') as f:
                self.author["bio"] = f.read()
        
        if os.path.exists("ebook/author/STORIES.md"):
            with open("ebook/author/STORIES.md", 'r', encoding='utf-8') as f:
                self.author["stories"] = f.read()

        if os.path.exists("ebook/author/AUTHOR_STYLE.md"):
            with open("ebook/author/AUTHOR_STYLE.md", 'r', encoding='utf-8') as f:
                self.author["master_style"] = f.read()

        # Load Author Styles Options
        for filepath in glob.glob("ebook/author/styles/*.md"):
            name = os.path.basename(filepath).replace(".md", "").lower()
            with open(filepath, 'r', encoding='utf-8') as f:
                self.author["styles"][name] = f.read()

        # Load Author Visions Options
        for filepath in glob.glob("ebook/author/visions/*.md"):
            name = os.path.basename(filepath).replace(".md", "").lower()
            with open(filepath, 'r', encoding='utf-8') as f:
                self.author["visions"][name] = f.read()

    def get_summary(self):
        return {
            "factory_rules": list(self.factory.keys()),
            "book_types": list(self.types.keys()),
            "author_styles": list(self.author["styles"].keys()),
            "author_visions": list(self.author["visions"].keys())
        }

if __name__ == "__main__":
    config = EbookConfig()
    print("--- 🏭 Inteligência da Fábrica Carregada ---")
    summary = config.get_summary()
    for key, val in summary.items():
        print(f"{key.replace('_', ' ').capitalize()}: {', '.join(val)}")
