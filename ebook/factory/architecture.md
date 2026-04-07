# Architecture Document - Ebook Generator

## 1. Visão Geral do Sistema
O sistema será estruturado como uma aplicação CLI modular.

## 2. Componentes Principais
- **Core Engine:** Responsável pelo processamento lógico e orquestração.
- **Parsers:** Módulos para ler diferentes formatos de entrada (Markdown, Text).
- **Renderers:** Módulos para gerar os arquivos de saída (PDF, EPUB, HTML).
- **Plugin System:** Para futuras extensões de estilos e integrações de IA.

## 3. Tech Stack Sugerida
- **Linguagem:** Node.js (TypeScript) ou Python (dependendo da preferência por bibliotecas de PDF).
- **Conversão:** Pandoc, Puppeteer ou bibliotecas nativas como `pdfkit`.

## 4. Fluxo de Dados
1. Input (Markdown/Config) -> 2. Parser -> 3. Internal Representation -> 4. Renderer -> 5. Output File (salvo em `output/`).
