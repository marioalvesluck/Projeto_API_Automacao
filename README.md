# Projeto_API_Automacao

Necessario Conhecimentos basicos em Python. 

Agradecimentos Jannsen livro Consumindo API .

Este Projeto tem como finalidade Auxiliar a comunidade nas automações do Ambiente Zabbix.

Versão Homologado : 5.4 <=

Necessario Para Ultilizaçao Package:
  - pip
  - setuptools
  - zabbix-api

- Alterar no Arquivo main.py , Linha Abaixo , Adicionando URL do Front do Zabbix , User - Senha.
  
control = C.Monitoramento("http://192.168.3.111/zabbix", "Admin", "zabbix")

[1] - Relatório de Grupos - 
     - Lista Grupo que Obtém host Ativo 
	    - ID - Grupo
	 
[2] - Listar hosts - Lista hosts com ID informado Do grupo
     - Lista hosts informando ID do Grupo  
        - HostID - Hostname - IP 

[3] - Listar triggers de um host 
     
	 - Lista Triggers do host informando ID
	    - TriggerID - Descrição

[4] - Listar triggers de um grupo 
    - Lista Triggers do grupo informando *item  
	- Opção Exportar para Planilha excell digitando nome Informado.
            - TriggerID
            - Hostname
			- IP
			- Descrição da triggers
			
[5] - Adicionar dependencia de Trigger
    - Informando TriggerID host *PAI * Opção4
	- Informar lista TriggerID dos hosts dependentes
	  * Observação Não Há limite triggerID.

[6] - Remover dependencia de Trigger
    - Informar Lista TriggerID .
       * Observação Não Há limite triggerID.	

[7] - Agentes desatualizados
    - Informa hosts que nao estao atualizados conforme versão Agente zabbix-server
		           
	           Em Desenvolvimento 
			   - Integrar Ambiente com ansible e Realizar Tarefas Atualizacao dos Agentes

[8] - Relatorio de Triggers

	           - Relatório de triggers com Acknowledged
			   - Relatório de triggers com Unacknowledged
			   - Relatório de triggers com ACK/UNACK
    
- Gerando ITservices - Em Desenvolvimento

	           - Gerando ITservice para todos os grupos e hosts, tags, sla.
			   - Gerando ITservice para todos os hosts de um grupo.
			   - Gerando ITservice selecionando grupos, hosts e itens,tags, sla.
			   - Deletar toda arvore de Itservice
			   
[10]- Relatorio de itens não suportados
    
	- Lista Itens Não Suportados
	  - Opção de Desativar
	
    - hostid
	- ItemID
	- key
	- Nome
    - Erro    