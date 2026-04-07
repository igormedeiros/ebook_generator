import base64
import json
import subprocess
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

msg = MIMEMultipart()
msg['To'] = 'igor.medeiros_bMKtAL@kindle.com'
msg['Subject'] = 'OpenClaw: Construindo Seu Próprio Jarvis (Versão Refatorada)'
msg['From'] = 'me'

text = MIMEText("Olá, Mestre! Segue o e-book refatorado e expandido para o seu Kindle.")
msg.attach(text)

with open('output/OpenClaw_Jarvis_Final.html', 'rb') as f:
    part = MIMEApplication(f.read(), Name='OpenClaw_Jarvis_Final.html')
part['Content-Disposition'] = 'attachment; filename="OpenClaw_Jarvis_Final.html"'
msg.attach(part)

raw_bytes = msg.as_bytes()
raw_b64 = base64.urlsafe_b64encode(raw_bytes).decode('utf-8')

payload = json.dumps({"raw": raw_b64})

try:
    result = subprocess.run(
        ["gws", "gmail", "users", "messages", "send", "--params", '{"userId": "me"}', "--json", payload],
        check=True
    )
    print("Email enviado com sucesso!")
except subprocess.CalledProcessError as e:
    print(f"Erro ao enviar. Exit code: {e.returncode}")
    sys.exit(1)
