# Orquestração do Workflow (FLOW.md)

Este documento define a máquina de estados da "Fábrica de Ebooks". Ele garante que o projeto possa ser retomado de qualquer ponto sem perda de contexto.

## 1. Princípio da Persistência Total
- **Nenhum comando de geração deve ser executado sem um arquivo de destino definido.**
- Antes de iniciar qualquer etapa, o agente deve ler o checkpoint da etapa anterior.
- Se o agente "esquecer" ou o contexto for limpo, os arquivos em `workspace/process/` são a única fonte da verdade.

## 1B. Configuração de Fonte (NotebookLM)
- **Obrigatório:** Antes de iniciar a definição do tema (`00-THEME.md`), o agente deve executar `nlm notebook list` e perguntar ao usuário qual notebook deve ser usado como fonte de conhecimento para o e-book.
- O ID ou Alias do notebook selecionado deve ser registrado no checkpoint `00B-SOURCE_NOTEBOOK.md`.
- Toda pesquisa e geração subsequente deve utilizar a skill `nlm-skill` para consultar esta base.

## 2. Ciclo de Interação
Para cada etapa do pipeline no `PRD.md`:
1. **Proposta:** O agente propõe o conteúdo da etapa com base nas specs e nas consultas ao NotebookLM.
2. **Aprovação:** O usuário valida, critica ou ajusta.
3. **Checkpoint:** O agente salva a versão final aprovada em `workspace/process/XX-NOME.md`.
4. **Transição:** O agente sinaliza que a etapa está concluída e sugere a próxima.

## 3. Estrutura de Checkpoints
- `00-THEME.md`: A semente do projeto.
- `00B-SOURCE_NOTEBOOK.md`: Definição obrigatória da fonte de conhecimento (ID/Alias do NotebookLM).
- `01-METADATA.md`: Identidade comercial.
- `01B-VISION.md`: Alma filosófica.
- `01C-STYLE.md`: Identidade editorial.
- `01D-TYPE.md`: Regras de gênero (ex: TECH).
- `02-AVATARS.md`: O público-alvo validado.
- `03-REQUIREMENTS.md`: O "stack" do livro.
- `04-OUTLINE.md`: O mapa dos 10 capítulos.
- `04B-DEEP_RESEARCH.md`: Insumos técnicos minerados e validados (**Obrigatório para Redação**).
- `05-RESEARCH_LOG.md`: O cérebro técnico do livro.
- `06-AVATAR_FEEDBACK.md`: A voz do leitor.
- `06B-EDITORIAL_REVIEW.md`: O filtro dos 21 especialistas (**Skill: ebook-reviewer**).
- `07-FINAL_AUDIT.md`: O selo de qualidade (15k-20k palavras).
- `07B-KINDLE_FORMAT.md`: Formatação estruturada (**Skill: ebook-kindle-formatter**).
- `07C-BIBLIOGRAPHY.md`: Consolidação de fontes e referências (**Skill: ebook-bibliographer**).
- `08-DELIVERY_LOG.md`: Comprovante de envio Kindle.

## 4. Portões de Qualidade (Quality Gates)
0. **Pesquisa Técnica Exaustiva:** Antes da redação de qualquer capítulo (Etapa 05), o agente deve consolidar os achados da internet e do NotebookLM no diretório `insumos/` e no checkpoint `04B-DEEP_RESEARCH.md`, seguindo o protocolo `DEEP_RESEARCHER.md`.
1. **Conformidade Editorial:** Toda geração de conteúdo deve consultar e aplicar rigorosamente os padrões definidos em `ebook/factory/EDITORIAL_STANDARDS.md`.
2. **Auditoria Crítica:** Antes de qualquer envio, a skill `ebook-reviewer` deve ser acionada para validar o manuscrito contra o `EBOOK_SPECS.md`, `EDITORIAL_STANDARDS.md` e a checklist de especialistas.
3. **Validação de Formatação e Referências:** O arquivo gerado pela skill `ebook-kindle-formatter` e a bibliografia consolidada pela skill `ebook-bibliographer` devem ser revisados visualmente para garantir integridade.
4. **Bloqueio de Envio:** O envio para o Kindle (Etapa 08) é **terminantemente proibido** se as etapas 06B, 07B e 07C não estiverem marcadas como aprovadas no log de checkpoint.

## 5. Recuperação de Erro
- Se um capítulo falhar na validação, o agente volta ao checkpoint `04B-DEEP_RESEARCH.md` para minerar novos dados ou ao `05-RESEARCH_LOG.md` e reescreve apenas o trecho afetado, gerando um novo log de revisão.
