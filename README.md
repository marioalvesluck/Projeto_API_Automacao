# Projeto_API_Automacao

Agradecimentos Jannsen livro Consumindo API .

Este Projeto tem como finalidade Auxiliar a comunidade nas automações do Ambiente Zabbix.

Versão Homologado : 5.4 <=

Necessario Para Ultilizaçao Package:
  - pip
  - setuptools
  - zabbix-api

- Alterar no Arquivo main.py , Linha Abaixo , Adicionando URL do Front do Zabbix , User - Senha.
  
control = C.Monitoramento("http://192.168.3.111/zabbix", "Admin", "zabbix")

O que obtém na Automação .

[1] - Relatório de Grupos
[2] - Listar hosts
[3] - Listar triggers de um host
[4] - Listar triggers de um grupos
    - Exportação de triggers para Arquivo CSV.
[5] - Adicionar dependencia de Trigger
[6] - Remover dependencia de Trigger
[7] - Agentes Desatualizados
[8] - Relatorio de Triggers
[9] - Gerando ITservices - Desenvolvimento
[10]- Relatorio de itens não suportados