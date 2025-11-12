<!-- instructions/INSTRUCTIONS-TITULO.md -->
# instructions/INSTRUCTIONS-TITULO.md
# 🧪 TITULO.md
> **Laboratório de Fórmulas para Geração de Títulos e Subtítulos**
> Regras e modelos para criar **títulos e subtítulos** para o eBook.
> Usa insumos de `INSTRUCTIONS-LIVROS_BASE.md` e `INSTRUCTIONS-OPINIOES_VISAO_AUTOR.md`.

---

## 🧭 FINALIDADE
Definir **fórmulas reproduzíveis** para:
- Gerar 10 opções de **título** a partir da **ideia central** definida no @ESPECIFICACOES.md.
- Escolher **3 finalistas** com base em critérios objetivos.
- Selecionar **1 vencedor**.
- Montar **subtítulo**.
- Produzir saídas padronizadas para uso direto no eBook.

> Objetivo: **consistência + clareza + apelo prático** para devs Python (Júnior → Sênior).

---

## 🧩 VARIÁVEIS DE ENTRADA
```yaml
tema_principal: "<ex.: LangChain na prática clínica>"
ideia_central: "<extraído do @ESPECIFICACOES.md>"
publico_alvo: ["Dev Python Júnior", "Pleno", "Sênior"]
palavras_chave: ["Agentes de IA", "RAG", "Saúde", "Produção", "Ética"]
beneficio_chave: "<o que o leitor ganha>"
diferencial_autor: "<experiência do Igor / visão humanista>"
livros_base: # dos 5 principais em LIVROS_BASE.md
  - {titulo: "...", autor: "...", ideia_forca: "..."}
  - ...
tom: ["técnico", "humano", "didático", "inspirador"]
```

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

---

## 🎨 GERAÇÃO DO PROMPT DA CAPA

Após a definição do **título vencedor** e do **subtítulo**, o próximo passo é a criação do prompt para a capa do eBook.

- **Ação**: Seguir as instruções do arquivo `@CAPA.md` para gerar um prompt detalhado.
- **Resultado**: O prompt gerado deve ser inserido no arquivo `@ESPECIFICACOES.md`, na seção `Especificação da Capa`.