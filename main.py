# -*- coding: utf-8 -*-

import monitoramento_zabbix as C
from os import system
import sys

control = C.Monitoramento("http://192.168.3.111/zabbix", "Admin", "zabbix")

GroupError = Exception


def err_hostgroup():
    print("Grupo não existe")
    input("Pressione ENTER para continuar")
    menu_itservice()
    menu_opcao_itservice()

def menu():
    if system('cls'):
        pass
    else:
        system('cls')

    print(" Escolha uma opção do menu ")
    print("[1] - Relatório de Grupos")
    print("[2] - Listar hosts")
    print("[3] - Listar triggers de um host")
    print("[4] - Listar triggers de um grupo")
    print("[5] - Adicionar dependencia de Trigger")
    print("[6] - Remover dependencia de Trigger")
    print("[7] - Agentes desatualizados")
    print("[8] - Relatorio de Triggers")
    print("[9] - Gerando ITservices - Desenvolvimento")
    print("[10]- Relatorio de itens não suportados")
    print ("[0]- Sair")
    menu_opcao()

def menu_triggers():
    system('cls')
    print("------ Escolha uma opção para o relatório ---")
    print( "[1] - Relatório de triggers com Acknowledged")
    print ("[2] - Relatório de triggers com Unacknowledged")
    print ("[3] - Relatório de triggers com ACK/UNACK")
    print ("[0] - Sair")
def menu_itservice():
    system('cls')
    print("--- Escolha uma opção para criar o ITservice ---")
    print("[1] - Gerando ITservice para todos os grupos e hosts")
    print("[2] - Gerando ITservice para todos os hosts de um grupo")
    print("[3] - Gerando ITservice selecionando grupos, hosts e itens")
    print("[4] - Deletar toda arvore de Itservice")
    print ("[0] - Sair")

def menu_opcao_itservice():
    opcao = str(input("Selecione uma opção: "))

    if opcao == '1':
        system("cls")
        confirma = str(input("Deseja confirmar s/n:  "))
        if confirma == "s":
            control.populate_all()
        print("\n")
        input("Pressione ENTER para continuar")
    if opcao == '2':
        system("cls")
        try:
            groupid = str(input("ID do grupo desejado:  ")).split(" ")
            if not control.get_hostgroups_name(groupid) in control.get_hostgroups():
                raise GroupError
            confirma = str(input("Deseja confirmar s/n:  "))
            if confirma == "s":
                control.populate_all(groupid)
        except GroupError:
            err_hostgroup()
        print("\n")
        input("Pressione ENTER para continuar")
    if opcao == '3':
        system("cls")
        try:
            groupid = str(input("ID do grupo desejado:  ")).split(" ")
            if not control.get_hostgroups_name(groupid) in control.get_hostgroups():
                raise GroupError
            hosts = str(input("ID dos hots desejados:  ")).split(" ")
            itens = str(input("itens desejados:  ")).split(" ")
            confirma = str(input("Deseja confirmar s/n:  "))
            if confirma == "s":
                control.populate_itens(groupid, hosts, itens)
        except GroupError:
            err_hostgroup()
        print("\n")
        input("Pressione ENTER para continuar")
    if opcao == '4':
        system("cls")
        confirma = str(input("Deseja confirmar s/n:  "))
        if confirma == "s":
            control.delete_tree_itservices()
        print("\n")
        input("Pressione ENTER para continuar")
    else:
        menu()

def menu_opcao():
    opcao = str(input("Selecione uma opção: "))
    if opcao == '1':
        system('cls') or system('cls')
        control.print_hostgroup()
        print("\n")
        input("Pressione ENTER para continuar")
        menu()
    elif opcao == '2':
        hostgroup_id = str(input("Digite o id grupo: "))
        system("cls")
        try:
            control.print_hosts(hostgroup_id)
            input("Pressione ENTER para continuar")
        except:
            print("ID inexistente!!!")
            input("Pressione ENTER para continuar")
        menu()
    elif opcao == '3':
        hostid = input("Digite o ID do host: ")
        system("cls")
        control.print_triggers_hosts(hostid)
        input("Pressione ENTER para continuar")
        menu()
    elif opcao == '4':
        grupo = input(str("Informe o ID do  grupo: "))
        itens = input("Informe os itens: ").split(" ")
        system("cls")
        control.get_hostgroup_items(itens, grupo=grupo)
        input("Pressione ENTER para continuar")
        menu()
    elif opcao == '5':
        id = input(str("Informe a TriggerID Host Pai: ")).split(" ")
        triggers = input("Informe a lista de TriggerIDs de Hosts dependentes: ").split(" ")
        system("cls")
        control.add_trigger_dependency(id_pai=id, triggers_ids=triggers)
        input("Pressione ENTER para continuar")
        menu()
    elif opcao == '6':
        triggers = input("Informe a lista de triggers que deseja remover de dependentes: ").split(" ")
        system("cls")
        control.del_trigger_dependency(triggers)
        input("Pressione ENTER para continuar")
        menu()
    elif opcao == '7':
        control.agentesDesatualizados()
        input("Pressione ENTER para continuar")
        menu()
    elif opcao == '8':
        menu_triggers()
        control.relatorio_triggers()
        menu()
    elif opcao == '9':
        menu_itservice()
        menu_opcao_itservice()
        menu()
    elif opcao == '10':
        system('cls')
        control.get_unsuported_itens()
        input("Pressione ENTER para continuar")
        menu()
    elif opcao == '0':
        sys.exit()
    else:
        menu()


menu()