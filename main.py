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

    print(" Choose an option from the Menu ")
    print("[1] - Group Report")
    print("[2] - List hosts")
    print("[3] - List triggers from a Host")
    print("[4] - List triggers from a Group")
    print("[5] - Add Trigger Dependency")
    print("[6] - Remove Trigger Dependency")
    print("[7] - Outdated Agents / Desatualizados ")
    print("[8] - Trigger Report")
    print("[9] - Generating ITservices - Development")
    print("[10]- Reporting unsupported items")
    print ("[0]- Exit")
    menu_opcao()

def menu_triggers():
    system('cls')
    print("------ Choose an option for the report ---")
    print( "[1] - Trigger report with Acknowledged")
    print ("[2] - Trigger reporting with Unacknowledged")
    print ("[3] - Trigger report with ACK/UNACK")
    print ("[0] - Exit")
def menu_itservice():
    system('cls')
    print("--- Choose an option to create the ITservice ---")
    print("[1] - Generating ITservice for all groups and hosts")
    print("[2] - Generating ITservice for all hosts in a Group")
    print("[3] - Generating ITservice by selecting groups, hosts and items")
    print("[4] - Delete all Itservice tree")
    print ("[0] - Exit")

def menu_opcao_itservice():
    opcao = str(input("Select an option: "))

    if opcao == '1':
        system("cls")
        confirma = str(input("Do you want to confirm y/n:  "))
        if confirma == "s":
            control.populate_all()
        print("\n")
        input("Press ENTER to Continue")
    if opcao == '2':
        system("cls")
        try:
            groupid = str(input("Desired group ID:  ")).split(" ")
            if not control.get_hostgroups_name(groupid) in control.get_hostgroups():
                raise GroupError
            confirma = str(input("Do you want to confirm y/n:  "))
            if confirma == "s":
                control.populate_all(groupid)
        except GroupError:
            err_hostgroup()
        print("\n")
        input("Press ENTER to Continue")
    if opcao == '3':
        system("cls")
        try:
            groupid = str(input("Desired group ID:  ")).split(" ")
            if not control.get_hostgroups_name(groupid) in control.get_hostgroups():
                raise GroupError
            hosts = str(input("Desired hots ID:  ")).split(" ")
            itens = str(input("Desired items:  ")).split(" ")
            confirma = str(input("Do you want to confirm y/n:  "))
            if confirma == "s":
                control.populate_itens(groupid, hosts, itens)
        except GroupError:
            err_hostgroup()
        print("\n")
        input("Press ENTER to Continue")
    if opcao == '4':
        system("cls")
        confirma = str(input("Do you want to confirm y/n:  "))
        if confirma == "s":
            control.delete_tree_itservices()
        print("\n")
        input("Press ENTER to continue")
    else:
        menu()

def menu_opcao():
    opcao = str(input("Select an option: "))
    if opcao == '1':
        system('cls') or system('cls')
        control.print_hostgroup()
        print("\n")
        input("Press ENTER to continue")
        menu()
    elif opcao == '2':
        hostgroup_id = str(input("Digite o id grupo: "))
        system("cls")
        try:
            control.print_hosts(hostgroup_id)
            input("Press ENTER to continue")
        except:
            print("ID inexistente!!!")
            input("Pressione ENTER para continuar")
        menu()
    elif opcao == '3':
        hostid = input("Digite o ID do host: ")
        system("cls")
        control.print_triggers_hosts(hostid)
        input("Press ENTER to continue")
        menu()
    elif opcao == '4':
        grupo = input(str("Informe o ID do  grupo: "))
        itens = input("Informe os itens: ").split(" ")
        system("cls")
        control.get_hostgroup_items(itens, grupo=grupo)
        input("Press ENTER to continue")
        menu()
    elif opcao == '5':
        id = input(str("Enter the Parent Host TriggerID: ")).split(" ")
        triggers = input("Enter the list of TriggerIDs of dependent Hosts: ").split(" ")
        system("cls")
        control.add_trigger_dependency(id_pai=id, triggers_ids=triggers)
        input("Press ENTER to continue")
        menu()
    elif opcao == '6':
        triggers = input("Enter the list of triggers you want to remove from Dependents: ").split(" ")
        system("cls")
        control.del_trigger_dependency(triggers)
        input("Press ENTER to continue")
        menu()
    elif opcao == '7':
        control.agentesDesatualizados()
        input("Press ENTER to continue")
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
        input("Press ENTER to continue")
        menu()
    elif opcao == '0':
        sys.exit()
    else:
        menu()


menu()