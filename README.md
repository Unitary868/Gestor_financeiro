💶 Gestor de Finanças Pessoais
Documento descritivo do projeto FinançasPro
🧠 Introdução
O presente projeto consiste no desenvolvimento de um sistema de gestão financeira pessoal denominado FinançasPro, implementado em Python. O objetivo principal é permitir ao utilizador registar, consultar e gerir as suas receitas e despesas, bem como acompanhar o saldo disponível e planear os seus gastos.
O sistema encontra-se organizado por módulos, garantindo uma estrutura clara, reutilizável e de fácil manutenção. Para além das entidades iniciais, o projeto integra agora as entidades Orçamento e Pagamento, tornando a aplicação mais completa e mais próxima de um contexto real de gestão financeira.
🧱 Estruturas de Dados
•	Dicionários (dict): utilizados para representar entidades como a conta, a transação, o orçamento e o pagamento, permitindo associar atributos a valores.
•	Listas (list): usadas para armazenar coleções de transações, pagamentos e orçamentos.
•	Tuplos (tuple): utilizados para estruturas imutáveis, como as categorias de transações.
•	Variáveis globais: permitem simular uma base de dados em memória durante a execução do programa.
🧑‍💼 Entidades do Sistema
👤 Entidade Conta
A entidade Conta representa o utilizador do sistema, sendo responsável pela autenticação e identificação.
Atributos:
•	id → identificador único
•	nome → nome do utilizador
•	nif → número de identificação fiscal
•	pin → código de autenticação
•	token → identificador de sessão
Função:
Permitir o registo e login do utilizador, garantindo acesso seguro ao sistema.
💸 Entidade Transação
A entidade Transação representa cada movimento financeiro realizado pelo utilizador, podendo corresponder a uma receita ou a uma despesa.
Atributos:
•	id → identificador único
•	tipo → receita ou despesa
•	descricao → descrição do movimento
•	valor → montante em euros
•	categoria → tipo de transação
Função:
Permitir o registo, edição, remoção e consulta de movimentos financeiros, sendo essencial para o cálculo do saldo e análise de gastos.
📊 Entidade Orçamento
A entidade Orçamento representa o planeamento financeiro do utilizador para um determinado período, ajudando a controlar limites de despesa por categoria ou por mês.
Atributos:
•	id → identificador único
•	categoria → categoria associada ao orçamento
•	limite → valor máximo definido
•	periodo → período de validade, por exemplo mensal
•	gasto_atual → valor já utilizado
Função:
Permitir ao utilizador definir limites de gasto e acompanhar se está dentro ou fora do valor previsto.
💳 Entidade Pagamento
A entidade Pagamento representa um pagamento efetuado pelo utilizador, associado a uma despesa ou a uma obrigação financeira específica.
Atributos:
•	id → identificador único
•	descricao → descrição do pagamento
•	valor → montante pago
•	data → data do pagamento
•	metodo → forma de pagamento, por exemplo numerário, cartão ou transferência
Função:
Registar pagamentos realizados, permitindo identificar quando e como um determinado valor foi pago.
⚙️ Funcionalidades (CRUD)
•	Create (Criar) → criação de conta, transações, orçamentos e pagamentos
•	Read (Ler) → consulta de dados, como extrato, saldo, conta, limites de orçamento e histórico de pagamentos
•	Update (Atualizar) → edição de transações, orçamentos e pagamentos
•	Delete (Eliminar) → remoção de transações, orçamentos e pagamentos
❌ Sistema de Erros
O sistema utiliza códigos inspirados em HTTP para representar estados e erros:
•	200 OK → operação realizada com sucesso
•	201 Created → recurso criado com sucesso
•	400 Bad Request → dados inválidos
•	401 Unauthorized → credenciais incorretas
•	404 Not Found → recurso inexistente
•	409 Conflict → conflito de dados
•	500 Internal Server Error → erro do sistema
🧰 Módulos do Sistema
•	main.py → interface principal e controlo do fluxo do programa
•	conta.py → gestão da entidade Conta
•	transacao.py → gestão da entidade Transação
•	orcamento.py → gestão da entidade Orçamento
•	pagamento.py → gestão da entidade Pagamento
•	utils.py → funções auxiliares, como validação, geração de IDs e tokens
🔄 Funcionamento Geral
•	O utilizador cria uma conta ou faz login.
•	Após autenticação, acede ao menu principal.
•	Pode registar receitas e despesas.
•	Pode definir orçamentos para diferentes categorias ou períodos.
•	Pode registar pagamentos efetuados.
•	Pode consultar o extrato, o saldo, os limites de orçamento e o histórico de pagamentos.
•	Pode editar ou apagar registos quando necessário.
🧠 Conclusão
O sistema FinançasPro demonstra uma implementação sólida de conceitos fundamentais de programação, incluindo estruturas de dados, modularização e operações CRUD. A utilização de códigos de erro inspirados em HTTP contribui para uma abordagem mais profissional e organizada, aproximando o funcionamento do sistema a aplicações reais.
Com a inclusão das entidades Orçamento e Pagamento, o projeto torna-se mais completo, pois passa a permitir não só o registo de movimentos financeiros, mas também o planeamento e o controlo dos gastos. Desta forma, o utilizador consegue gerir as suas finanças de forma simples, eficiente e estruturada, cumprindo os objetivos propostos.
