# Projeto_API_Automacao


Este Projeto tem como finalidade Auxiliar a comunidade nas automações do Ambiente Zabbix.

Necessario Para Ultilizaçao Package:
  - pip
  - setuptools
  - zabbix-api

- Alterar no Arquivo main.py , Linha Abaixo.
  
control = C.Monitoramento("http://192.168.3.111/zabbix", "Admin", "zabbix")

O que obtém na Automação até Momento.

[1] - Relatório de Grupos
[2] - Listar hosts
[3] - Listar triggers de um host
[4] - Listar triggers de um grupo
[5] - Adicionar dependencia de Trigger
[6] - Remover dependencia de Trigger
[7] - Agentes desatualizados
[8] - Relatorio de Triggers
[9] - Gerando ITservices - Desenvolvimento
[10]- Relatorio de itens não suportados