---
name: email-send
description: "Send an email using msmtp."
metadata:
  version: 0.1.0
  openclaw:
    category: "productivity"
    requires:
      bins:
        - msmtp
---

# Send Email via msmtp

Send an email using the `msmtp` command. This skill assumes `msmtp` is already configured in the environment.

## Usage

```bash
printf "To: <TO>\nSubject: <SUBJECT>\n\n<BODY>" | msmtp <TO>
```

### With Attachments (using `mutt` or raw MIME)

Para enviar anexos, é recomendado usar o `msmtp` como MTA (Mail Transfer Agent) para ferramentas que geram MIME corretamente, ou construir a mensagem MIME manualmente.

Exemplo de uso básico:
```bash
printf "To: igor.medeiros_bMKtAL@kindle.com\nSubject: E-book\n\nOlá, mestre!" | msmtp igor.medeiros_bMKtAL@kindle.com
```

## Security

- Never log or print the email contents or credentials.
- Ensure the recipient is authorized.

> [!CAUTION]
> This is a **write** command — confirm with the user before executing.
