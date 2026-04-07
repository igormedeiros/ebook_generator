from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

msg = MIMEMultipart()
msg['To'] = 'igor.medeiros_bMKtAL@kindle.com'
msg['Subject'] = 'OpenClaw: Guia Definitivo (Limpo)'
msg['From'] = 'me'

text = MIMEText("Olá, Mestre! Esta é a versão rigorosamente limpa, sem nenhuma tag {#...} no texto. Melissa na dedicatória e 2026 no copyright.")
msg.attach(text)

with open('output/OpenClaw_Guia_Sem_Tags.html', 'rb') as f:
    part = MIMEApplication(f.read(), Name='OpenClaw_Guia_Sem_Tags.html')
part['Content-Disposition'] = 'attachment; filename="OpenClaw_Guia_Sem_Tags.html"'
msg.attach(part)

with open('output/raw_message.eml', 'wb') as f:
    f.write(msg.as_bytes())
