# -*- coding: utf-8 -*-

from zabbix_api import ZabbixAPI
import datetime, time


class Monitoramento(ZabbixAPI):
    def __init__(self, url, login, senha):
        self.zapi = self.conexao_api(url, login, senha)
        self.server = url

    def conexao_api(self, url, login, senha):
        try:
            zapi = ZabbixAPI(server=url, timeout=180)
            zapi.login(login, senha)
            print("Conectando na API do Zabbix Versão:{}".format(zapi.api_version()))
            return zapi
        except Exception as err:
            print("Falha ao conectar na API do Zabbix")
            print("Erro:{}".format(err))

    def get_hostgroups(self,groupid=""):
        hostgroups = self.zapi.hostgroup.get({
            "output": ['name'],
            'monitored_hosts': 1,
            "filter": {"groupid": groupid}
        })
        listaGrupos = []
        for x in hostgroups:
            hostgroup_name = x['name']
            listaGrupos.append(hostgroup_name)
        return listaGrupos

    def get_hostgroups_id(self, grupo):
        groupId = self.zapi.hostgroup.get({"output": "extend", "filter": {"name": grupo}})[0]['groupid']
        return groupId

    def get_hostgroups_name(self, grupoid):
        groupName = self.zapi.hostgroup.get({"output": "extend", "filter": {"groupid": grupoid}})[0]["name"]
        return groupName

    def get_hostid(self, host):
        # retorna o id de um determinado host
        hostId = self.zapi.host.get({"output": "hostid", "filter": {"host": host}})[0]['hostid']
        return hostId

    def get_hosts(self, grupo,hostid=""):
        hosts_grupo = self.zapi.host.get({"groupids": self.get_hostgroups_id(grupo), "output": ["host"],"filter":{"hostid": hostid }})
        listaHosts = []
        for x in hosts_grupo:
            listaHosts += [x['host']]
        return listaHosts

    def get_hostname(self, hostid):
        hostName = self.zapi.host.get({"output": "extend", "filter": {"hostid": hostid}})[0]["host"]
        return hostName

    def print_hosts(self, grupo_id):
        hosts = self.get_hosts(self.get_hostgroups_name(grupo_id))
        for x in hosts:
            host_interface = self.zapi.hostinterface.get({"output": ["ip"], "hostids": self.get_hostid(x)})
            host_ip = host_interface[0]["ip"]
            print("HostID: {} Nome: {} IP: {}\n".format(self.get_hostid(x), x, host_ip))

    def get_items_hosts(self, host, keys=""):
        items = self.zapi.item.get(
            {"hostids": self.get_hostid(host), "with_triggers": True, "selectTriggers": "extend","filter":{"key_":keys}})
        listaItems = []
        for x in items:
            listaItems += [x['key_']]
        return listaItems

    def get_item_triggerid(self, host, item):
        triggerId = self.zapi.item.get(
            {"output": "triggers", "hostids": self.get_hostid(host), "with_triggers": True,
             "selectTriggers": "triggers",
             "filter": {"key_": item}})[0]['triggers'][0]['triggerid']
        return triggerId

    def get_item_triggerName(self, host, item):
        triggerName = self.zapi.item.get(
            {"output": "extend", "hostids": self.get_hostid(host), "with_triggers": True, "selectTriggers": "triggers",
             "filter": {"key_": item}})[0]["name"]
        return triggerName

    def criar_csv(self, lista_dados, csv_name="arquivo.csv"):
        arquivo = open(csv_name, "w")
        arquivo.write("TriggerID, Nome do host, IP, Descrição\r\n")
        for i in lista_dados:
            arquivo.writelines(i)
            arquivo.writelines("\n")

    def get_triggers_hosts(self, host_id):
        # recebe um hostid como parametro e retorna todas as triggers
        triggers = self.zapi.trigger.get({
            "output": ["description"],
            "hostids": host_id,
            "selectItems": ["key_", "name"],
            "monitored": "true",
            "expandDescription": True,

        })
        return triggers

    def get_hostgroup_items(self, lista_triggers, grupo):
        # percorre a lista de hosts atribuindo nome id e nome visível as respectivas variáveis
        lista_triggers = lista_triggers

        hosts = self.zapi.host.get({"output": ['host', 'name'], "groupids": grupo})
        lista_dados = []
        for x in hosts:
            descricao = ""
            triggerid = ""
            host_id = x['hostid']
            host_name = x['host']
            # atribui a host_interface uma lista contendo um dicionario com id e numero ip do host
            host_interface = self.zapi.hostinterface.get({"output": ["ip"], "hostids": host_id})
            # chama uma funcao que percorre todas as triggers a cada ciclo do loop inicial

            host_ip = host_interface[0]["ip"]

            lista_dados.append(" ," + host_name)

            for itens in self.get_triggers_hosts(host_id):
                # se a chave contida em items for igual a icmpping mostra na tela as informações e adiciona a triggerid a uma lista
                for j in lista_triggers:
                    if itens["items"][0]["key_"] == j:
                        print("Nome: {} TriggerID: {}\nIP: {} Descrição: {}\n".format(host_name, itens["triggerid"], host_ip,itens["description"]))
                descricao = itens["description"]
                triggerid = itens["triggerid"]

                info = triggerid + ", " + host_name + ", " + host_ip + ", " + descricao

                if not lista_dados.__contains__(info) and triggerid != "":
                    lista_dados.append(info)

        resposta = input("Deseja gerar o relatorio s/n ? ")
        if resposta == "s":
            csv_name = input("Digite o nome do CSV: ") + ".csv"
            self.criar_csv(lista_dados, csv_name=csv_name)

    # recebe uma lista de triggers pais e triggers filhos e adiciona as dependencias
    def add_trigger_dependency(self, id_pai, triggers_ids):
        trigger_ids = triggers_ids
        id_pai = id_pai
        id_dependentes = {}
        for pai in id_pai:
            for filhos in trigger_ids:
                try:
                    self.zapi.trigger.adddependencies({
                        # ID FILHO
                        "triggerid": str(filhos),
                        # ID PAI
                        "dependsOnTriggerid": str(pai)
                    })
                except:
                    id_dependentes[str(pai)] = str(filhos)

        print("ids que possuem dependencia {}".format(id_dependentes))

    # recebe uma lista de triggers e remove as dependencias
    def del_trigger_dependency(self, triggers_ids):
        trigger_ids = triggers_ids
        for i in trigger_ids:
            self.zapi.trigger.deleteDependencies({
                # ID FILHO
                "triggerid": str(i),
            })

    def agentesDesatualizados(self):
        itens = self.zapi.item.get({
            "filter": {"key_": "agent.version"},
            "output": ["lastvalue", "hostid"],
            "templated": False,
            "selectHosts": ["host"],
            "sortorder": "ASC"
        })

        try:
            versaoZabbixServer = self.zapi.item.get({
                "filter": {"key_": "agent.version"},
                "output": ["lastvalue", "hostid"],
                "hostids": "10084"
            })[0]["lastvalue"]

            print('{0:6} | {1:30}'.format("Versão", "Host"))

            for x in itens:
                if x['lastvalue'] != versaoZabbixServer and x['lastvalue'] <= versaoZabbixServer:
                    print('{0:6} | {1:30}'.format(x["lastvalue"], x["hosts"][0]["host"]))


        except IndexError:
            print("Não foi possível obter a versão do agent no Zabbix Server.")

    def relatorio_triggers(self):
        params = {'output': ['triggerid', 'lastchange', 'comments', 'description'], 'selectHosts': ['hostid', 'host'],
                  'expandDescription': True, 'only_true': True, 'active': True}

        opcao = input("[+] - Selecione uma opção[0-3]: ")

        if opcao == '1':
            params['withAcknowledgedEvents'] = True
            label = 'ACK'
        elif opcao == '2':
            params['withUnacknowledgedEvents'] = True
            label = 'UNACK'
        elif opcao == '3':
            label = 'ACK/UNACK'
        elif opcao == '0':
            input("\nPressione ENTER para voltar")

        hoje = datetime.date.today()

        try:
            global tmp_trigger
            tmp_trigger = int(input("[+] - Selecione qual o tempo de alarme (dias): "))
        except Exception:
            input("\nPressione ENTER para voltar")
        dt = (hoje - datetime.timedelta(days=tmp_trigger))
        conversao = int(time.mktime(dt.timetuple()))
        operador = input("[+] - Deseja ver Triggers com mais ou menos de {0} dias [ + / - ] ? ".format(tmp_trigger))

        if operador == '+':
            params['lastChangeTill'] = conversao
        elif operador == '-':
            params['lastChangeSince'] = conversao
        else:
            input("\nPressione ENTER para voltar")
        rel_ack = self.zapi.trigger.get(params)
        for relatorio in rel_ack:
            lastchangeConverted = datetime.datetime.fromtimestamp(float(relatorio["lastchange"])).strftime(
                '%Y-%m-%d %H:%M')

            print("Trigger {} com {} de {} dias".format(label, operador, tmp_trigger))
            print("=" * 80)
            print("Nome da Trigger: ", relatorio["description"],
                  "| HOST:" + relatorio["hosts"][0]["host"] + " | ID:" + relatorio["hosts"][0]["hostid"])
            print("Hora de alarme: ", lastchangeConverted)
            print("URL da trigger: {}/zabbix.php?action=problem.view&filter_set=1&filter_triggerids%5B%5D={}".format(
                self.server, relatorio["triggerid"]))
            print("Descrição da Trigger: ", relatorio["comments"])
        print("\nTotal de {} triggers encontradas".format(rel_ack.__len__()))
        opcao = input("\nDeseja gerar relatorio em arquivo? [s/n]")

        if opcao == 's' or opcao == 'S':
            with open("relatorio_triggers.csv", "w") as arquivo:
                arquivo.write("Nome da Trigger,Hora de alarme:,URL da trigger:,Descrição da Trigger:\r\n ")
                for relatorio in rel_ack:
                    arquivo.write(str(relatorio))
                    arquivo.write(
                        ("| HOST:" + relatorio["hosts"][0]["host"] + " | ID:" + relatorio["hosts"][0]["hostid"]))
                    arquivo.write(",")
                    arquivo.write(lastchangeConverted)
                    arquivo.write(",")
                    arquivo.write(
                        "{}/zabbix.php?action=problem.view&filter_set=1&filter_triggerids%5B%5D={}".format(self.server,
                                                                                                           relatorio[
                                                                                                               "triggerid"]))
                    arquivo.write(",")
                    arquivo.write(("\"" + relatorio["comments"] + "\""))
                    arquivo.write("\r\n")
            input("\nArquivo gerado com sucesso ! Pressione ENTER para voltar")
        else:
            input("\nPressione ENTER para voltar")

    def create_dad_itservices(self, grupo):
        self.zapi.service.create({"name": grupo, "algorithm": "1", "showsla": "1", "goodsla": "99", "sortorder": "1"})

    def create_itservice_pid(self, grupo):
        parentId = \
            self.zapi.service.get({"selectParent": "extend", "selectTrigger": "extend", "expandExpression": "true",
                                   "filter": {"name": grupo}})[0]['serviceid']
        return parentId

    def create_child_itservices(self, host, grupo):
        self.zapi.service.create({"name": host, "algorithm": "1", "showsla": "1", "goodsla": "99.99", "sortorder": "1",
                                  "parentid": self.create_itservice_pid(grupo)})

    def create_itservice_pid_child(self, host):
        parentIdChild = self.zapi.service.get(
            {"selectParent": "extend", "selectTrigger": "extend", "expandExpression": "true",
             "filter": {"name": host}})[0]['serviceid']
        return parentIdChild

    def create_child_itservices_trigger(self, host, item):
        self.zapi.service.create(
            {"name": self.get_item_triggerName(host, item), "algorithm": "1", "showsla": "1", "goodsla": "99.99",
             "sortorder": "1", "parentid": self.create_itservice_pid_child(host),
             "triggerid": self.get_item_triggerid(host, item)})

    def get_itservices(self):
        itServices = self.zapi.service.get({"selectParent": "extend", "selectTrigger": "extend"})
        listaServicos = []
        for x in itServices:
            listaServicos += [x['serviceid']]
        return listaServicos
    def get_unsuported_itens(self):
        itens = self.zapi.item.get({"output": "extend", "monitored": "true", "filter": {"state": 1}})
        print("===============================================================================================")
        print("ID   ITEMID        NOME           ERRO")
        print("===============================================================================================")

        for x in itens:
            print("HOSTID: {},ITEMID: {},KEY: {},NOME: {},ERROR:{}".format(x["hostid"], x["itemid"], x["key_"], x["name"],x["error"]))
        # print(itens)
        print("============================================")
        print("Total de itens não suportados: ", len(itens))
        print("============================================")

        if len(itens) != 0:
            confirma = str(input("Deseja desabilitar os itens não suportados s/n:  "))
            if confirma == "s":
                for x in itens:
                    self.zapi.item.update({"itemid": x['itemid'], "status": 1})
                print("Itens desabilitados!!!")

    def delete_tree_itservices(self):
        for x in self.get_itservices():
            self.zapi.service.deletedependencies([x])
            self.zapi.service.delete([x])

    def populate_all(self, hostgroupid=""):
        for nomeGrupo in self.get_hostgroups(groupid=hostgroupid):
            self.create_dad_itservices(nomeGrupo)
            for nomeHost in self.get_hosts(nomeGrupo):
                self.create_child_itservices(nomeHost, nomeGrupo)
                print(nomeHost)
                for nomeItem in self.get_items_hosts(nomeHost):
                    self.create_child_itservices_trigger(nomeHost, nomeItem)


    def populate_itens(self,groupid,hosts,itens):
        for nomeGrupo in [self.get_hostgroups_name(groupid)]:
            self.create_dad_itservices(nomeGrupo)
            for nomeHost in self.get_hosts(nomeGrupo,hostid=hosts):
                self.create_child_itservices(nomeHost, nomeGrupo)
                print(nomeHost)
                for nomeItem in self.get_items_hosts(nomeHost,keys=itens):
                    self.create_child_itservices_trigger(nomeHost, nomeItem)

    def get_sla(self):
        sla = self.zapi.service.getsla({
            "serviceids": "631",
            "intervals": [{"from": 1570536000, "to": 1570543200}]})

        return sla

    def print_triggers_hosts(self, host):
        triggers = self.zapi.trigger.get(
            {"hostids": host, "expandDescription": "true", "expandComment": "true", "expandExpression": "true"})
        for x in triggers:
            print("TriggerID: {} Descrição: {} ".format(x["triggerid"], x["description"]))
        return triggers

    def print_hostgroup(self):
        for x in self.get_hostgroups():
            hostgroup_id = self.get_hostgroups_id(x)
            print('{} - {}'.format(hostgroup_id, x))




# a = Monitoramento("http://192.168.0.253/zabbix", "Admin", "zabbix")

# print(a.get_hostgroups(24))

# a.delete_tree_itservices()
# a.populate_all()
# print(a.get_hostgroups_name([24]))

# print(a.get_hostgroups_name(24))
# a.populate_itens("24","10278",["icmpping","icmppingloss"])
# print(a.get_hosts(a.get_hostgroups_name(24),hostid=["10278","10279"]))