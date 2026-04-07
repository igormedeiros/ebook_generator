import subprocess
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

TO_EMAIL = 'igor.medeiros_bMKtAL@kindle.com'
SUBJECT = 'O Agente Invisível: Guia Prático OpenClaw v2026.3.31'
FILE_PATH = 'workspace/dominando-openclaw-guia-pratico/O_AGENTE_INVISIVEL_KINDLE.html'
FILE_NAME = 'O_AGENTE_INVISIVEL_KINDLE.html'

msg = MIMEMultipart()
msg['To'] = TO_EMAIL
msg['Subject'] = SUBJECT

body = "Olá, Comandante! Segue a versão final e auditada do e-book 'O Agente Invisível' para o seu Kindle. Boa leitura e soberania!"
msg.attach(MIMEText(body, 'plain'))

try:
    with open(FILE_PATH, 'rb') as f:
        part = MIMEApplication(f.read(), Name=FILE_NAME)
    part['Content-Disposition'] = f'attachment; filename="{FILE_NAME}"'
    msg.attach(part)

    # Envia via msmtp
    process = subprocess.Popen(['msmtp', TO_EMAIL], stdin=subprocess.PIPE)
    process.communicate(input=msg.as_bytes())

    if process.returncode == 0:
        print("✅ E-book enviado para o Kindle com sucesso via msmtp!")
    else:
        print(f"❌ Erro ao enviar e-mail. Código de saída: {process.returncode}")
        sys.exit(process.returncode)

except FileNotFoundError:
    print(f"❌ Arquivo não encontrado: {FILE_PATH}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Ocorreu um erro inesperado: {str(e)}")
    sys.exit(1)
