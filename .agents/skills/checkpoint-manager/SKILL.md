---
name: checkpoint-manager
description: Gerencia a persistência de progresso em projetos de engenharia e redação através de arquivos Markdown de checkpoint. Use sempre que concluir uma etapa importante, antes de interrupções longas ou para consolidar o estado atual de um workspace complexo.
---

# Checkpoint Manager

Este skill orienta a criação e manutenção de checkpoints estruturados para garantir que qualquer agente possa retomar o trabalho exatamente de onde ele parou, sem perda de contexto técnico ou estratégico.

## Padrão de Nomenclatura e Localização

- **Formato:** `XX-CHECKPOINT_NAME.md` (onde XX é um número sequencial, ex: `07-FINAL_AUDIT.md`).
- **Localização:** Obrigatoriamente dentro da pasta `process/` do projeto no `workspace/`.

## Estrutura Obrigatória do Checkpoint

Todo arquivo de checkpoint deve conter as seguintes seções:

1. **Cabeçalho de Status:**
   - **Status:** [Iniciado | Em Progresso | Pendente | Concluído]
   - **Data:** AAAA-MM-DD
   - **Projeto:** Nome do diretório no workspace.

2. **Resumo do Progresso:**
   - Lista clara do que foi realizado desde o último checkpoint.
   - Referência a arquivos gerados ou modificados.

3. **Mapa de Contexto (Estado Atual):**
   - Localização dos rascunhos, insumos e arquivos finais.
   - Status de autenticação em ferramentas externas (ex: NotebookLM, GitHub).

4. **Pendências Críticas (To-Do List):**
   - Lista de tarefas imediatas necessárias para finalizar a etapa atual.

5. **Próximos Passos:**
   - Instrução clara para o próximo agente sobre por onde começar.

## Gatilhos de Uso

Invoque este skill e gere um novo checkpoint quando:
- Terminar a redação ou revisão de um bloco de capítulos.
- Consolidar insumos de pesquisa em um documento de processo.
- Encontrar erros de infraestrutura ou autenticação que exijam intervenção humana.
- Antes de encerrar uma sessão de trabalho longa.

## Melhores Práticas

- **Seja Específico:** Evite termos vagos como "progredimos no livro". Prefira "Capítulo 02 redigido em ch02.md, validado contra insumos técnicos".
- **Persistência de Erros:** Registre falhas conhecidas (ex: "Auth NotebookLM expirada") para que o próximo agente não perca tempo tentando ferramentas que ele já sabe que não funcionam.
- **Linkagem:** Sempre inclua o caminho completo dos arquivos citados.
