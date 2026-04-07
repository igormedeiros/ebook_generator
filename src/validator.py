import subprocess
import sys
import os

def check_pandoc():
    try:
        version = subprocess.check_output(['pandoc', '--version']).decode().split('\n')[0]
        print(f"✅ Pandoc encontrado: {version}")
        return True
    except FileNotFoundError:
        print("❌ Pandoc NÃO encontrado. Por favor, instale-o (https://pandoc.org/installing.html)")
        return False

def check_python_version():
    if sys.version_info >= (3, 10):
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} encontrado.")
        return True
    else:
        print("❌ Python 3.10 ou superior é necessário.")
        return False

def check_directories():
    required_dirs = ['ebook/specs', 'ebook/types', 'ebook/author', 'workspace/process', 'output']
    for d in required_dirs:
        if os.path.exists(d):
            print(f"✅ Diretório '{d}' presente.")
        else:
            print(f"❌ Diretório '{d}' ausente.")

if __name__ == "__main__":
    print("--- Validando Ambiente da Fábrica de Ebooks ---\n")
    python_ok = check_python_version()
    pandoc_ok = check_pandoc()
    check_directories()
    
    if python_ok and pandoc_ok:
        print("\n🚀 Plataforma pronta para iniciar a produção!")
    else:
        print("\n⚠️ O ambiente ainda não está 100% pronto. Verifique os erros acima.")
