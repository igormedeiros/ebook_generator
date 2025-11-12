<!-- instructions/INSTRUCTIONS-ESTUDOS_DE_CASO.md -->
# instructions/INSTRUCTIONS-ESTUDOS_DE_CASO.md
# 🧠 ESTUDOS_DE_CASO.md
> Template completo para **estudos de caso aplicados** — unindo teoria, prática e contexto real.  
> Cada estudo de caso deve ser criado a partir de **pesquisas recentes no Google** (fontes técnicas, reprodutíveis e verificáveis).

---

## 🎯 Objetivo
Transformar o conteúdo técnico do capítulo em **aprendizado prático e memorável**.  
O estudo de caso é onde o leitor:
- Vê como o conceito é aplicado no mundo real.  
- Entende impactos e resultados mensuráveis.  
- Aprende com problemas e soluções reais.

> Cada capítulo do eBook deve conter **um estudo de caso relevante** — preferencialmente baseado em situações autênticas encontradas por meio do Google.

---

## 🌐 Fontes de Pesquisa

Para cada estudo de caso, busque no **Google**:

### 1️⃣ Pesquisa Direta
Procure:
> `"case study" + <tema do capítulo> + Python`  
> `"real world example" + <tópico>`  
> `"project" + <biblioteca principal>`  
> `"use case" + <framework ou ferramenta>`  

Use operadores para refinar resultados:
- `site:medium.com`, `site:towardsdatascience.com`, `site:realpython.com`
- `filetype:pdf` para relatórios técnicos
- `"case study" AND "Python" AND "<tema>"`  

Priorize:
- Artigos técnicos (Medium, Dev.to, Real Python, Analytics Vidhya, Towards Data Science).  
- Repositórios GitHub com estudos documentados.  
- Papers e relatórios práticos com código aberto.  

### 2️⃣ Critérios de Seleção
- O caso deve ter sido publicado **nos últimos 2 anos**.  
- Deve conter **código ou métricas reproduzíveis**.  
- Deve ilustrar **um conceito técnico abordado no capítulo**.  
- Deve oferecer **um aprendizado prático**, não apenas teórico.

---

## 🧱 Estrutura Padrão de Estudo de Caso

```markdown
# 🧠 Estudo de Caso — Capítulo <NN>: <Título do Capítulo Exemplo>

> Fonte principal: Pesquisa Google  
> Nível: 🟨 / 🟥  

---

## 📍 Contexto
Descreva brevemente o problema real:
- Onde ocorreu (empresa, laboratório, projeto open-source).  
- Qual a situação inicial e o desafio técnico.  
- Quais foram as metas e limitações do projeto.

---

## 🧩 Conceito Central Aplicado
Explique **qual conceito técnico** foi aplicado no caso.  
> Exemplo: “Aplicação de [CONCEITO TÉCNICO] para [OBJETIVO] em [CONTEXTO].”

Inclua links diretos para as fontes consultadas (Google, artigos, repositórios).

---

## 💻 Implementação Prática
Descreva como o conceito foi implementado:
- Bibliotecas e frameworks utilizados ([BIBLIOTECA 1], [FRAMEWORK 1], etc.).  
- Arquitetura textual ou pseudodiagrama para ilustrar a solução.  
- Código mínimo reproduzível.

```python
# capitulo_<NN>/estudo_caso_exemplo.py
# [INSIRA AQUI UM EXEMPLO DE CÓDIGO MÍNIMO REPRODUZÍVEL]
```

---

## 📈 Resultados Obtidos

| Indicador         | Antes | Depois | Impacto         |
| ----------------- | ----- | ------ | --------------- |
| [INDICADOR 1]     | [VALOR] | [VALOR] | [IMPACTO]       |
| [INDICADOR 2]     | [VALOR] | [VALOR] | [IMPACTO]       |

Inclua também **resultados qualitativos**, como melhoria de legibilidade, modularidade ou performance.

---

## 🧠 Lições Aprendidas

* O que o caso ensina de forma prática.
* Quais boas práticas foram confirmadas.
* Quais erros ou armadilhas foram evitados.
* Como o conceito pode ser reaplicado em outros contextos.

💡 *Exemplo:*

> “[INSIRA UMA LIÇÃO APRENDIDA COM O ESTUDO DE CASO].”

---

## 📚 Referências

* [Google] Artigo original: <link>
* [GitHub] Repositório relacionado: <link>
* [Docs oficiais] <link se aplicável>

---

## 💬 Insight Pessoal

> “Ao estudar este caso, percebi que [INSIRA UM INSIGHT PESSOAL AQUI].”
> — [NOME DO AUTOR]

````

---

## 🔍 Automação e Metadados (YAML)
> Estrutura útil para rastrear e gerar estudos de caso automaticamente a partir das pesquisas no Google.

```yaml
- id: estudo_caso-<capitulo>
  titulo: "Automação de Tarefas Clínicas com Python"
  fonte_principal:
    origem: "google"
    link: "https://towardsdatascience.com/automation-python-healthcare"
    data: "2024-09"
  conceito_principal: "Automação de processos repetitivos com Python"
  bibliotecas:
    - "pandas"
    - "fastapi"
    - "langchain"
  indicadores:
    - nome: "Tempo de execução"
      antes: "15s"
      depois: "2.5s"
      impacto: "83% de melhoria"
  aprendizado_chave: "Automatizar tarefas médicas com Python requer validação e logging adequados."
  nivel: "pleno"
````

---

## 🧩 Boas Práticas para Criação de Casos

1. **Priorize Google como principal fonte.**

   * Pesquise globalmente e refine resultados com operadores.
   * Leia mais de uma fonte antes de redigir.

2. **Dê crédito sempre.**

   * Cite explicitamente os links, autores e repositórios.
   * Prefira fontes com exemplos reprodutíveis.

3. **Evite teoria.**

   * O estudo de caso é prático, narrativo e objetivo.
   * Trate-o como uma mini história real, com começo, meio e fim.

4. **Traga contexto humano.**

   * Explique *por que* a solução foi necessária.
   * Relacione a experiência com o aprendizado do leitor.

5. **Use métricas e evidências.**

   * Sempre que possível, inclua dados de tempo, desempenho ou linhas de código.
   * Evite frases vagas (“melhorou muito”); prefira números.

6. **Área de Aplicação Recomendadas**

   * Saúde e tecnologia médica 🏥
   * Automação e produtividade 💡
   * Inteligência Artificial 🤖
   * Ciência de dados e análise 📊
   * Engenharia de software 🧱

---

## ✅ Checklist de Qualidade

* [ ] Pesquisa feita no Google (últimos 2 anos).
* [ ] Fontes técnicas, originais e citadas corretamente.
* [ ] Código ou arquitetura reprodutível incluídos.
* [ ] Resultados numéricos ou qualitativos apresentados.
* [ ] Lições práticas e insights claros.
* [ ] Tom humano, técnico e inspirador.

---

> 💬 *“Todo conceito ganha sentido quando atravessa o mundo real.”*
> — *Igor Medeiros*

```