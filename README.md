💶 Gestor de Finanças Pessoais
🧠 Introdução

O presente projeto consiste no desenvolvimento de um sistema de gestão financeira pessoal denominado FinançasPro, implementado em Python. O objetivo principal é permitir ao utilizador registar, consultar e gerir as suas receitas e despesas, bem como acompanhar o saldo disponível.

O sistema encontra-se organizado por módulos, garantindo uma estrutura clara, reutilizável e de fácil manutenção.

🧱 Estruturas de Dados

O sistema utiliza diferentes estruturas de dados fundamentais:

Dicionários (dict): utilizados para representar entidades como a conta e cada transação, permitindo associar atributos a valores.
Listas (list): usadas para armazenar coleções de transações.
Tuplos (tuple): utilizados para estruturas imutáveis, como as categorias de transações.
Variáveis globais: permitem simular uma base de dados em memória durante a execução do programa.
🧑‍💼 Entidades do Sistema
👤 Entidade Conta

A entidade Conta representa o utilizador do sistema, sendo responsável pela autenticação e identificação.

Atributos:

id → identificador único
nome → nome do utilizador
nif → número de identificação fiscal
pin → código de autenticação
token → identificador de sessão

Função:
Permitir o registo e login do utilizador, garantindo acesso seguro ao sistema.

💸 Entidade Transação

A entidade Transação representa cada movimento financeiro realizado pelo utilizador, podendo corresponder a uma receita ou a uma despesa.

Atributos:

id → identificador único
tipo → receita ou despesa
descricao → descrição do movimento
valor → montante em euros
categoria → tipo de transação

Função:
Permitir o registo, edição, remoção e consulta de movimentos financeiros, sendo essencial para o cálculo do saldo e análise de gastos.

⚙️ Funcionalidades (CRUD)

O sistema implementa operações CRUD (Create, Read, Update, Delete):

Create (Criar) → criação de conta e transações
Read (Ler) → consulta de dados (extrato, saldo, conta)
Update (Atualizar) → edição de transações
Delete (Eliminar) → remoção de transações

❌Entidades Sistema de Erros

O sistema utiliza códigos inspirados em HTTP para representar estados e erros:

200 OK → operação realizada com sucesso
201 Created → recurso criado com sucesso
400 Bad Request → dados inválidos
401 Unauthorized → credenciais incorretas
404 Not Found → recurso inexistente
409 Conflict → conflito de dados
500 Internal Server Error → erro do sistema

🧰 Módulos do Sistema
main.py → interface principal e controlo do fluxo do programa
conta.py → gestão da entidade Conta
transacao.py → gestão da entidade Transação
utils.py → funções auxiliares (validação, IDs, tokens)

🔄 Funcionamento Geral
O utilizador cria uma conta ou faz login
Após autenticação, acede ao menu principal
Pode registar receitas e despesas
Pode consultar o extrato e saldo
Pode editar ou apagar transações

🧠 Conclusão

O sistema FinançasPro demonstra uma implementação sólida de conceitos fundamentais de programação, incluindo estruturas de dados, modularização e operações CRUD. A utilização de códigos de erro inspirados em HTTP contribui para uma abordagem mais profissional e organizada, aproximando o funcionamento do sistema a aplicações reais.

Além disso, o projeto permite ao utilizador gerir as suas finanças de forma simples e eficiente, cumprindo os objetivos propostos.
