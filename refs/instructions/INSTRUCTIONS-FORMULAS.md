<!-- instructions/INSTRUCTIONS-FORMULAS.md -->
# instructions/INSTRUCTIONS-FORMULAS.md
# 🧪 FORMULAS.md
> **Laboratório de Fórmulas para Geração Editorial**  
> Regras e modelos para criar **títulos, subtítulos, estruturas de capítulos, hooks**, slugs e metadados do eBook.  
> Usa insumos de `INSTRUCTIONS-LIVROS_BASE.md`, `INSTRUCTIONS-OPINIOES_VISAO_AUTOR.md` e `INSTRUCTIONS-CAPITULOS.md`.

---

## 🧭 FINALIDADE
Definir **fórmulas reproduzíveis** para:
- Gerar 10 opções de **título** a partir da ideia central.
- Escolher **3 finalistas** com base em critérios objetivos.
- Selecionar **1 vencedor**.
- Montar **subtítulo**, **estrutura de capítulos**, **hooks** e **slugs**.
- Produzir saídas padronizadas para uso direto no eBook.

> Objetivo: **consistência + clareza + apelo prático** para devs Python (Júnior → Sênior).

---

## 🧩 VARIÁVEIS DE ENTRADA
```yaml
tema_principal: "<ex.: LangChain na prática clínica>"
ideia_central: "<enunciado curto e claro>"
publico_alvo: ["Dev Python Júnior", "Pleno", "Sênior"]
palavras_chave: ["Agentes de IA", "RAG", "Saúde", "Produção", "Ética"]
beneficio_chave: "<o que o leitor ganha>"
diferencial_autor: "<experiência do Igor / visão humanista>"
livros_base: # dos 5 principais em LIVROS_BASE.md
  - {titulo: "...", autor: "...", ideia_forca: "..."}
  - ...
tom: ["técnico", "humano", "didático", "inspirador"]
````

---

## 🧠 ABSTRAÇÃO DE TÍTULOS (derivada dos 5 livros)

Extraia padrões dos livros principais (ver `LIVROS_BASE.md`):

* **Pattern A (How-to + Transformação):** `Como <Resultado> com <Ferramenta/Abordagem>`
* **Pattern B (X em Ação):** `<Tecnologia> em Ação: <Aplicação/Contexto>`
* **Pattern C (Promessa + Evidência):** `<Resultado> com <Técnica> — <Prova/Âmbito>`
* **Pattern D (Do Zero ao Pro):** `Do Zero ao <Resultado> com <Ferramenta> em <Tempo/Passos>`
* **Pattern E (Fórmula Híbrida Ética):** `<Tecnologia> que Cuida: <Aplicação> com <Princípio Ético>`

> Dica: combine **verbo de ação + benefício tangível + contexto** (ex.: saúde/produção).

---

## 🧮 FÓRMULA DE GERAÇÃO DE TÍTULOS (10 opções)

Para cada **pattern** acima, gere variações usando:

* `<tema_principal>`, `<ideia_central>`, `<beneficio_chave>`, `<palavras_chave[0..2]>`.

**Template de saída (lista):**

```yaml
titulos_sugeridos:
  - "Como <beneficio_chave> com <tema_principal>"
  - "<tema_principal> em Ação: <aplicação_concreta>"
  - "<beneficio_chave> com <tecnica>: <contexto>"
  - "Do Zero ao <resultado> com <ferramenta> em <N passos>"
  - "<Tecnologia> que Cuida: <aplicação> com <princípio>"
  - "<Resultado> no Mundo Real: <tema_principal> para Devs Python"
  - "Campo de Batalha: <tema_principal> na Produção"
  - "Blueprint <tema_principal>: do Lab ao Prod"
  - "Playbook de <tema_principal> para <publico_alvo>"
  - "Pragmática <tema_principal>: problemas reais, soluções limpas"
```

---

## 📊 SCORING DOS TÍTULOS (3 finalistas → 1 vencedor)

Atribua **0–5** em cada eixo; calcule `score_total = soma(pesos * notas)`:

```yaml
pesos:
  clareza: 0.25       # entendimento imediato
  beneficio: 0.25     # promessa concreta ao leitor
  especificidade: 0.20# termos técnicos/ contexto real
  memorabilidade: 0.15# ritmo/sonoridade
  alinhamento_visao: 0.15 # OPINIOES_VISAO_AUTOR.md
```

**Matriz de avaliação (exemplo):**

```yaml
avaliacao_titulos:
  - titulo: "LangChain em Ação: Agentes de IA para Saúde"
    notas: {clareza: 5, beneficio: 4, especificidade: 5, memorabilidade: 4, alinhamento_visao: 5}
    score_total: 4.6
  - ...
finalistas: ["...", "...", "..."]
vencedor: "<melhor score_total>"
```

> Observação: quando houver dados de tendências (SEO/communities), adicionar eixo **tendencia_busca (0.10)** e **recalibrar pesos** (reduzir outros proporcionalmente).

---

## 🧾 FÓRMULA DE SUBTÍTULO (expansão do título vencedor)

**Estrutura:**

```
<o que é> + <para quem> + <como/abordagem> + <resultado prático> + (opcional: ethos)
```

**Template:**

```
"Um guia prático para desenvolvedores Python (Júnior a Sênior) construírem <solucao> com <tecnologia>, indo do laboratório à produção, com ética, clareza e código comentado."
```

---

## 🧱 FÓRMULA DA ESTRUTURA DE CAPÍTULO

Cada capítulo deve seguir:

1. **Hook (2–4 linhas):** dor/benefício/contexto real.
2. **Objetivos de Aprendizado (bullet curto).**
3. **Mapa do Território (o que será coberto).**
4. **Conceitos Essenciais (curto, direto, com analogias leves).**
5. **Exemplos de Código (PEP 8 + comentário da 1ª linha):**

   * `# capitulo_XX/nome_exemplo.py`
6. **Cenário Real / Estudo de Caso (mini-case).**
7. **Checklist de Produção (ação objetiva).**
8. **Exercícios (5 múltipla escolha + gabarito comentado).**
9. **Desafio Final (sem resposta).**
10. **Resumo e Links (documentação oficial + cruzamentos com LIVROS_BASE).**

---

## 🎣 FÓRMULA DE HOOK (abertura de capítulo)

* **Estrutura:** `dor → obstáculo → virada → promessa`.
* **Template:**
  “Você precisa <resultado>, mas <obstaculo>. Neste capítulo, você verá como <técnica> remove <bloqueio> e te leva a <promessa> em <X passos>.”

---

## 🧰 FÓRMULA DE CHECKLIST PRÁTICO

```yaml
checklist:
  - "Configurar <dependencia>"
  - "Rodar teste mínimo: <comando>"
  - "Salvar artefato: <path/arquivo>"
  - "Validar métrica: <nome>=<limiar>"
  - "Documentar variações: <README trecho>"
```

---

## 🧪 FÓRMULA DE EXERCÍCIOS (múltipla escolha)

Para cada capítulo, gere 5 questões:

```yaml
q: "<pergunta direta sobre ponto-chave>"
a: ["A", "B", "C", "D"]
correta: "<letra>"
comentario: "Por que a correta é correta; por que as demais não são.""
```

**Desafio sem resposta (final do capítulo):**

```
"Implemente <X> em <contexto real> variando <parametros>. Documente decisões e trade-offs."
```

---

## 🗺️ FÓRMULA DE PLANEJAMENTO DOS 10 CAPÍTULOS

1. Fundamentos e vocabulário mínimo.
2. Ferramentas-base e ambiente.
3. Caso simples end-to-end.
4. Conceitos intermediários e variações.
5. Boas práticas e testes.
6. Integração com dados reais.
7. Prod/observabilidade/segurança.
8. Otimizações e custos.
9. Casos avançados e pitfalls.
10. Conclusão, próximos passos e roadmap.

> Ajuste a ordem conforme “processo de aprendizado” do público.

---

## 🔖 FÓRMULA DE NOMENCLATURA (slug, arquivos, figuras)

* **Slug do livro:** `slug = normalizar(titulo_vencedor).lower().replace(" ", "-")`
* **Pastas:**

  * `resultados/<slug>/manuscrito/`
  * `resultados/<slug>/figuras/`
  * `resultados/<slug>/codigo/`
* **Código exemplo:** `# capitulo_03/rag_pipeline_basico.py`
* **Figura:** `fig_cap03_fluxo_rag.png`

---

## 🧷 FÓRMULA DE METADADOS (YAML)

```yaml
ebook:
  titulo: "<vencedor>"
  subtitulo: "<subtitulo_gerado>"
  autor: "Igor Medeiros"
  publico: ["Dev Python Júnior", "Pleno", "Sênior"]
  palavras_chave: ["Python", "Agentes de IA", "RAG", "Saúde", "Produção"]
  slug: "<auto>"
  arquivos:
    raiz: "resultados/<slug>/"
    manuscrito: "resultados/<slug>/manuscrito/"
    codigo: "resultados/<slug>/codigo/"
    figuras: "resultados/<slug>/figuras/"
  referencias:
    livros_base: "LIVROS_BASE.md"
    visao_autor: "OPINIOES_VISAO_AUTOR.md"
```

---

## 🧪 EXEMPLO RÁPIDO (preenchimento)

```yaml
tema_principal: "[TEMA PRINCIPAL DO EBOOK]"
ideia_central: "[IDEIA CENTRAL DO EBOOK]"
beneficio_chave: "[BENEFÍCIO CHAVE PARA O LEITOR]"
titulos_sugeridos:
  - "[TÍTULO SUGERIDO 1]"
  - "[TÍTULO SUGERIDO 2]"
  - "[TÍTULO SUGERIDO 3]"
avaliacao_titulos:
  - titulo: "[TÍTULO SUGERIDO 1]"
    notas: {clareza: 5, beneficio: 5, especificidade: 5, memorabilidade: 4, alinhamento_visao: 5}
    score_total: 4.8
finalistas: ["[TÍTULO FINALISTA 1]",
             "[TÍTULO FINALISTA 2]",
             "[TÍTULO FINALISTA 3]"]
vencedor: "[TÍTULO VENCEDOR]"
subtitulo: "[SUBTÍTULO GERADO]"
```

---

## ✅ CHECKLIST FINAL

* [ ] 10 títulos gerados por **patterns**.
* [ ] Avaliação por **scoring** → 3 finalistas → 1 vencedor.
* [ ] Subtítulo gerado por fórmula.
* [ ] Estrutura de capítulo aplicada (hook, objetivos, exemplos, case, exercícios, desafio).
* [ ] Slugs, pastas e metadados preenchidos.
* [ ] Referências cruzadas com `LIVROS_BASE.md` e `OPINIOES_VISAO_AUTOR.md`.

---

## 🧩 YAML DE CONTROLE EDITORIAL

```yaml
tipo_documento: "formulas_editoriais"
versao: 1.0
autor: "Igor Medeiros"
dependencias:
  - "LIVROS_BASE.md"
  - "OPINIOES_VISAO_AUTOR.md"
  - "CAPITULOS.md"
saida_padrao:
  - "titulos_sugeridos"
  - "avaliacao_titulos"
  - "finalistas"
  - "vencedor"
  - "subtitulo"
  - "estrutura_capitulo"
status: "pronto_para_uso"
```