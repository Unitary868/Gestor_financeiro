FinançasPro – Gestor Financeiro
1. Introdução
O projeto FinançasPro consiste num sistema de gestão financeira pessoal desenvolvido em Python. O objetivo é permitir ao utilizador gerir receitas, despesas, metas de poupança e atividades profissionais de forma simples através de uma interface em terminal. O sistema está dividido em módulos: entidades, operações, menus e utilitários.
2. Entidades do Sistema
As principais entidades são:
- Conta: representa o utilizador (id, nome, nif, pin, token)
- Transação: representa movimentos financeiros (id, tipo, descrição, valor, categoria)
3. Estruturas de Dados
O sistema utiliza várias estruturas:
- Listas: para armazenar transações e metas
- Dicionários: para representar entidades
- Tuplos: para categorias e empregos (imutáveis)
- Variáveis globais: para gerar IDs únicos
4. CRUD
O sistema implementa CRUD:
- Create: criar conta, transações e metas
- Read: listar e visualizar dados
- Update: editar transações e atualizar metas
- Delete: apagar transações e metas
5. Funcionalidades
O sistema permite:
- Criar conta e login
- Adicionar receitas e despesas
- Consultar extrato
- Editar e apagar transações
- Criar e gerir metas
- Simular trabalho para ganhar dinheiro
- Ver resumo financeiro
6. Lógica do Sistema
O saldo é calculado com base nas transações. As metas permitem acompanhar progresso de poupança. Os empregos geram receitas com base em horas e valor por hora.
7. Interface
O sistema utiliza menus interativos em terminal com loops e condições para navegação.
8. Validação
O sistema valida dados como NIF, PIN, password e valores numéricos para evitar erros.
9. Conclusão
O FinançasPro é um sistema completo que demonstra uso de entidades, estruturas de dados e operações CRUD, sendo adequado para projetos académicos.
