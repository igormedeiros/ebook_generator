# Protocolo de Pesquisa Profunda (DEEP_RESEARCHER.md)

Este documento define como o agente deve minerar, cruzar e salvar dados antes de iniciar a redação de qualquer capítulo. O objetivo é garantir densidade técnica e atualidade.

## 1. Fontes Obrigatórias
Para cada capítulo do e-book, o agente deve realizar uma busca em duas frentes:
1.  **Interna (NotebookLM):** Consulta exaustiva ao notebook selecionado no início do projeto usando a `nlm-skill`.
2.  **Externa (Web):** Busca por notícias, documentações oficiais, tendências de mercado e alertas de segurança dos últimos 60 dias via `google_web_search`.

## 2. Consolidação de Insumos
- Todos os dados coletados devem ser salvos em arquivos `.md` individuais dentro da pasta `workspace/<slug-do-ebook>/insumos/`.
- Cada arquivo de insumo deve conter a fonte (URL ou ID do NotebookLM) e a data da coleta.

## 3. O Checkpoint 04B (DEEP_RESEARCH.md)
O resultado final desta etapa é o arquivo `workspace/process/04B-DEEP_RESEARCH.md`, que deve conter:
- Resumo executivo dos achados técnicos para cada capítulo do Sumário.
- Glossário de termos técnicos atualizados.
- Lista de "Cicatrizes de Produção" (erros comuns mapeados na pesquisa).
- Alertas de segurança ou mudanças de API detectadas.

## 4. Regra de Ouro
A escrita de um capítulo só pode ser iniciada se os insumos correspondentes em `insumos/` e o resumo em `04B-DEEP_RESEARCH.md` estiverem presentes e validados.