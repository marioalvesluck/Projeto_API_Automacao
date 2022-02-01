# -*- coding: utf-8 -*-

from zabbix_api import ZabbixAPI


def conexao_api(url, login, senha):
    try:
        zapi = ZabbixAPI(server=url, timeout=180)
        zapi.login(login, senha)
        print("Conectando na API do Zabbix Versão:{}".format(zapi.api_version()))
        return zapi
    except Exception as err:
        print("Falha ao conectar na API do Zabbix")
        print("Erro:{}".format(err))

zapi = conexao_api("http://192.168.0.253/zabbix", "Admin","zabbix")

def it_grupos():
    global zapi
    hostgroups = zapi.hostgroup.get({"output": "extend","monitored_hosts":1})
    listaGrupos = []
    for x in hostgroups:
        listaGrupos += [x['name']]
    return listaGrupos

def it_hostgroups_id(grupo):
    groupId = zapi.hostgroup.get({"output": "extend","filter":{"name":grupo}})[0]['groupid']
    return groupId

def it_hosts(grupo):
    hosts_grupo = zapi.host.get({"groupids":it_hostgroups_id(grupo), "output":["host"]})
    listaHosts = []
    for x in hosts_grupo:
        print (x['host'])
        listaHosts += [x['host']]
    return listaHosts

def it_hostid(host):
    hostId = zapi.host.get({"output":"hostid","filter":{"host":host}})[0]['hostid']
    return hostId

def it_triggers_hosts(host):
    triggers = zapi.trigger.get({"hostids":it_hostid(host), "expandDescription": "true", "expandComment": "true", "expandExpression": "true"})
    for x in triggers:
        print (x['description'])

def it_items_hosts(host,keys = ""):
    items = zapi.item.get({"hostids":it_hostid(host), "with_triggers":True, "selectTriggers": "extends","filter":{"key_":keys}})
    listaItems = []
    for x in items:
        listaItems += [x['key_']]
    return listaItems

def it_item_name(host, item):
    triggerId = zapi.item.get({"output":"extend","hostids":it_hostid(host), "with_triggers":True, "selectTriggers": "triggers", "filter":{"key_":item}})[0]["name"]
    return triggerId

def it_item_triggerid(host, item):
    triggerId = zapi.item.get({"output":"triggers","hostids":it_hostid(host), "with_triggers":True, "selectTriggers": "triggers", "filter":{"key_":item}})[0]['triggers'][0]['triggerid']
    return triggerId

def mk_pai_itservices(grupo):
    zapi.service.create({"name":grupo,"algorithm":"1","showsla":"1","goodsla":"99.99","sortorder":"1"})

def it_itservice_pid(grupo):
    parentId = zapi.service.get({"selectParent":"extend","selectTrigger":"extend","expandExpression":"true","filter":{"name":grupo}})[0]['serviceid']
    return parentId

def mk_filhos_itservices(host, grupo):
    zapi.service.create({"name":host,"algorithm":"1","showsla":"1","goodsla":"99.99","sortorder":"1","parentid":it_itservice_pid(grupo)})

def it_itservice_pid_child(host):
    parentIdChild = zapi.service.get({"selectParent":"extend","selectTrigger":"extend","expandExpression":"true","filter":{"name":host}})[0]['serviceid']
    return parentIdChild

def mk_filho_itservices_trigger(host, item):

    zapi.service.create({"name":it_item_name(host, item), "algorithm": "1", "showsla": "1", "goodsla": "99.99", "sortorder": "1", "parentid":it_itservice_pid_child(host), "triggerid":it_item_triggerid(host, item)})

def it_itservices():
    itServices = zapi.service.get({"selectParent":"extend","selectTrigger":"extend"})
    listaServicos = []
    for x in itServices:
        listaServicos += [x['serviceid']]
    return listaServicos

def delete_tree_itservices():
    for x in it_itservices():
        zapi.service.deletedependencies([x])
        zapi.service.delete([x])

def mk_populate_all():
    for nomeGrupo in it_grupos():
        mk_pai_itservices(nomeGrupo)
        for nomeHost in it_hosts(nomeGrupo):
            mk_filhos_itservices(nomeHost, nomeGrupo)
            for nomeItem in it_items_hosts(nomeHost):
                mk_filho_itservices_trigger(nomeHost, nomeItem)

def get_hostname(hostid):
    hostName = zapi.host.get({"output":"extend","filter":{"hostid":hostid}})[0]["host"]
    return hostName
def get_hostgroups_name(grupoid):
    groupName = zapi.hostgroup.get({"output": "extend","filter":{"groupid":grupoid}})[0]["name"]
    return groupName

# delete_tree_itservices()
# mk_populate_all()


print(it_items_hosts("Zabbix server",keys=["agent.hostname"]))
print(it_items_hosts("desk01",keys=["icmpping","icmppingloss"]))


def populate_all(self):
    for nomeGrupo in self.hostgroups:
        self.create_dad_itservices(nomeGrupo)
        self.get_g()
        for nomeHost in self.get_hosts(nomeGrupo):
            self.create_child_itservices(nomeHost, nomeGrupo)
            for nomeItem in self.get_items_hosts(nomeHost):
                self.create_child_itservices_trigger(nomeHost, nomeItem)




