from nornir import InitNornir
from pyzabbix import ZabbixAPI

# Zabbix API credentials
zapi = ZabbixAPI(url='http://localhost/zabbix/', user='Admin', password='zabbix')



def get_zabbix_hosts():
    # Retrieve hosts using Zabbix API
    hosts = zapi.host.get(output=['host', 'name', 'status'])

    # Create Nornir inventory dictionary
    inventory = {}
    for host in hosts:
        hostname = host['host']
        inventory[hostname] = {
            'hostname': hostname,
            'name': host['name'],
            'status': host['status']
        }

    return inventory


def main():
    # Retrieve Zabbix hosts and create Nornir inventory
    inventory = get_zabbix_hosts()

    # Initialize Nornir with the obtained inventory
    nr = InitNornir(inventory=inventory)

    # Execute tasks on the retrieved devices
    result = nr.run(task=my_task)

    # Print Nornir task results
    print(result)


def my_task(task):
    # Example task: Print device information
    print(f"Hostname: {task.host.hostname}")
    print(f"Name: {task.host.name}")
    print(f"Status: {task.host.status}")
    print("------------------")


if __name__ == "__main__":
    main()
