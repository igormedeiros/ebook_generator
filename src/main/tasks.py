"""
Definições de prompts para cada etapa do pipeline de escrita.
Utiliza LangChain 1.0+ para execução de agentes.
"""

# Prompts para cada etapa do ebook
INTRODUCTION_PROMPT = """
Escreva a introdução de um livro sobre autoconhecimento e inteligência emocional.
Apresente o tema central, o que o leitor pode esperar e a importância do autoconhecimento
e da inteligência emocional. Use uma história breve e envolvente que capture a atenção.

Output esperado:
Uma introdução motivacional e reflexiva, com uma história envolvente, sobre a importância
de entender e gerenciar emoções e explorar o valor do autoconhecimento.
"""

PROBLEMA_PROMPT = """
Neste capítulo, aborde o problema que o livro se propõe a resolver. Fale sobre os desafios
que as pessoas enfrentam em relação ao autoconhecimento e à gestão emocional. Discuta as
consequências de não lidar com as emoções adequadamente e como isso afeta a vida pessoal
e profissional.

Output esperado:
Uma explicação detalhada dos problemas enfrentados pelas pessoas com relação ao autoconhecimento
e à gestão emocional, incluindo exemplos práticos de como essas questões impactam diferentes áreas da vida.
"""

IDENTIFICACAO_PROMPT = """
Utilize histórias pessoais para criar uma conexão emocional com o leitor. Compartilhe experiências
que mostram como as pessoas lidaram com suas próprias emoções e os desafios que enfrentou. Isso ajudará os leitores
a se identificarem e a se sentirem mais confortáveis em explorar suas próprias emoções.

Output esperado:
Histórias pessoais que criam uma conexão emocional com o leitor, destacando os desafios enfrentados e como
essas situações podem ser aplicadas ao desenvolvimento emocional de cada pessoa.
"""

SOLUCAO_PROMPT = """
Apresente um método ou uma abordagem que os leitores possam seguir. Dê um nome ao método e, se possível,
crie um acrônimo que seja fácil de lembrar. Explique passo a passo como aplicar essa solução no cotidiano,
usando exemplos práticos para facilitar a compreensão. Essa seção deve ser clara e direta, oferecendo aos
leitores ferramentas concretas para trabalhar em seu autoconhecimento e inteligência emocional.

Output esperado:
Um método prático para os leitores seguirem, com explicações passo a passo de como aplicar as estratégias
no dia a dia, incluindo exemplos que facilitem a compreensão e implementação.
"""

PROTECAO_PROMPT = """
Alerte os leitores sobre comportamentos que podem minar o progresso que eles podem fazer seguindo seu método.
Discuta as armadilhas comuns que as pessoas enfrentam e como evitá-las. Essa seção é vital para garantir que os
leitores tenham consciência de que, mesmo com as melhores intenções, algumas ações podem ser prejudiciais.

Output esperado:
Uma análise das armadilhas mais comuns que podem atrapalhar o progresso dos leitores, com dicas claras de como
evitar esses comportamentos prejudiciais e manter o foco no desenvolvimento emocional.
"""

PERMISSAO_PROMPT = """
Forneça uma permissão psicológica aos leitores. Reforce que eles merecem ser felizes e que têm o
direito de buscar o melhor para si. Use frases inspiradoras que encorajem os leitores a acreditarem em seu potencial
para mudar e alcançar os resultados prometidos. Isso ajudará a criar um espaço seguro para que eles se sintam capazes
de seguir em frente.

Output esperado:
Mensagens inspiradoras e de incentivo que reforcem o direito dos leitores de buscarem a felicidade e o bem-estar,
dando a eles a segurança para perseguirem mudanças positivas em suas vidas.
"""

POTENCIA_PROMPT = """
Finalize com uma celebração! Motive os leitores a abraçarem a mudança e a aplicarem o que aprenderam. Use uma
linguagem poderosa e energizante para encorajar a ação e reforçar a ideia de que eles estão no caminho certo.
Essa seção deve deixar o leitor com um sentimento de empoderamento e determinação para continuar sua jornada de
autoconhecimento e desenvolvimento pessoal.

Output esperado:
Um texto final motivacional que celebre o progresso dos leitores e os encoraje a continuar aplicando as práticas de
autoconhecimento e inteligência emocional no dia a dia, com linguagem poderosa e energizante.
"""