from crewai import Task
from main.agents import writer_agent
from main.tools import ReplaceTextInDocxTool as replace_tool

# Task que o agente deve realizar
write_introduction_task = Task(
    description=(
        "Escreva a introdução de um livro sobre autoconhecimento e inteligência emocional. "
        "Apresente o tema central, o que o leitor pode esperar e a importância do autoconhecimento "
        "e da inteligência emocional. Use uma história breve e envolvente que capture a atenção."
    ),
    expected_output=(
        "Uma introdução motivacional e reflexiva, com uma história envolvente, sobre a importância "
        "de entender e gerenciar emoções e explorar o valor do autoconhecimento."
    ),
    agent=writer_agent,
    tools=[replace_tool] # Todo: Adicionar ferramentas de pesquisa em artigos científicos que evidenciam o conceito
    # rag tool que busque histórias inspiradoras que mostram a importância do tema
)
s
# Task: Problema - Descrever os desafios relacionados ao autoconhecimento e gestão emocional
task_problema = Task(
    description=(
        "Neste capítulo, aborde o problema que o livro se propõe a resolver. Fale sobre os desafios "
        "que as pessoas enfrentam em relação ao autoconhecimento e à gestão emocional. Discuta as "
        "consequências de não lidar com as emoções adequadamente e como isso afeta a vida pessoal "
        "e profissional."
    ),
    expected_output=(
        "Uma explicação detalhada dos problemas enfrentados pelas pessoas com relação ao autoconhecimento "
        "e à gestão emocional, incluindo exemplos práticos de como essas questões impactam diferentes áreas da vida."
    ),
    agent=writer_agent,
    tools=[replace_tool]  # Todo: Adicionar ferramentas de pesquisa sobre números e estatísticas que evidenciam o problema
)

# Task: Identificação - Conectar o leitor com experiências pessoais
task_identificacao = Task(
    description=(
        "Utilize histórias pessoais suas para criar uma conexão emocional com o leitor. Compartilhe experiências "
        "que mostram como você lidou com suas próprias emoções e os desafios que enfrentou. Isso ajudará os leitores "
        "a se identificarem com você e a se sentirem mais confortáveis em explorar suas próprias emoções."
    ),
    expected_output=(
        "Histórias pessoais que criam uma conexão emocional com o leitor, destacando os desafios enfrentados e como "
        "essas situações podem ser aplicadas ao desenvolvimento emocional de cada pessoa."
    ),
    agent=writer_agent,
    tools=[replace_tool]  # Todo: Adicionar ferramentas RAG de histórias de superação pessoal do Igor que estão relacionadas ao tema
)

# Task: Solução - Apresentar um método prático para os leitores
task_solucao = Task(
    description=(
        "Apresente um método ou uma abordagem que os leitores possam seguir. Dê um nome ao método e, se possível, "
        "crie um acrônimo que seja fácil de lembrar. Explique passo a passo como aplicar essa solução no cotidiano, "
        "usando exemplos práticos para facilitar a compreensão. Essa seção deve ser clara e direta, oferecendo aos "
        "leitores ferramentas concretas para trabalhar em seu autoconhecimento e inteligência emocional."
    ),
    expected_output=(
        "Um método prático para os leitores seguirem, com explicações passo a passo de como aplicar as estratégias "
        "no dia a dia, incluindo exemplos que facilitem a compreensão e implementação."
    ),
    agent=writer_agent,
    tools=[replace_tool]  # Todo: Adicionar ferramentas de pesquisa sobre métodos eficazes sobre o tema
)

# Task: Proteção - Alertar sobre comportamentos prejudiciais
task_protecao = Task(
    description=(
        "Alerte os leitores sobre comportamentos que podem minar o progresso que eles podem fazer seguindo seu método. "
        "Discuta as armadilhas comuns que as pessoas enfrentam e como evitá-las. Essa seção é vital para garantir que os "
        "leitores tenham consciência de que, mesmo com as melhores intenções, algumas ações podem ser prejudiciais."
    ),
    expected_output=(
        "Uma análise das armadilhas mais comuns que podem atrapalhar o progresso dos leitores, com dicas claras de como "
        "evitar esses comportamentos prejudiciais e manter o foco no desenvolvimento emocional."
    ),
    agent=writer_agent,
    tools=[replace_tool]  # Todo: Adicionar ferramentas de pesquisa sobre comportamentos autossabotadores e como evitá-los
)

# Task: Permissão - Oferecer uma permissão psicológica para buscar felicidade
task_permissao = Task(
    description=(
        "Neste capítulo, forneça uma permissão psicológica aos leitores. Reforce que eles merecem ser felizes e que têm o "
        "direito de buscar o melhor para si. Use frases inspiradoras que encorajem os leitores a acreditarem em seu potencial "
        "para mudar e alcançar os resultados prometidos. Isso ajudará a criar um espaço seguro para que eles se sintam capazes "
        "de seguir em frente."
    ),
    expected_output=(
        "Mensagens inspiradoras e de incentivo que reforcem o direito dos leitores de buscarem a felicidade e o bem-estar, "
        "dando a eles a segurança para perseguirem mudanças positivas em suas vidas."
    ),
    agent=writer_agent,
    tools=[replace_tool]  # Todo: Adicionar ferramentas de pesquisa sobre exemplos da permissão psicológica para o desejo do leitor
)

# Task: Potência - Encorajar a ação e celebração das conquistas
task_potencia = Task(
    description=(
        "Finalize com uma celebração! Motive os leitores a abraçarem a mudança e a aplicarem o que aprenderam. Use uma "
        "linguagem poderosa e energizante para encorajar a ação e reforçar a ideia de que eles estão no caminho certo. "
        "Essa seção deve deixar o leitor com um sentimento de empoderamento e determinação para continuar sua jornada de "
        "autoconhecimento e desenvolvimento pessoal."
    ),
    expected_output=(
        "Um texto final motivacional que celebre o progresso dos leitores e os encoraje a continuar aplicando as práticas de "
        "autoconhecimento e inteligência emocional no dia a dia, com linguagem poderosa e energizante."
    ),
    agent=writer_agent,
    tools=[replace_tool]  # Todo: Adicionar ferramentas de pesquisa sobre técnicas de motivação e celebração de conquistas
)