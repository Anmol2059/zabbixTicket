import os
import json
from pyzabbix import ZabbixAPI
import datetime

# Connect to the Zabbix API
zapi = ZabbixAPI('http://182.93.91.116/zabbix/')
zapi.login("Admin", "zabbix")

# Get the hosts and their status
hosts = zapi.host.get(output=['hostid', 'name', 'status'])

host_data = []  # Store host data

for host in hosts:
    host_id = host['hostid']
    host_name = host['name']
    host_status = host['status']

    status_emoji = "🟢" if host_status == "0" else "🔴"
    status_text = "on" if host_status == "0" else "off"

    # Get current timestamp
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    host_info = {
        'Timestamp': current_time,
        'Hostname': host_name,
        'Status': status_text,
        'StatusEmoji': status_emoji
    }

    host_data.append(host_info)

# Disconnect from the Zabbix API
zapi.user.logout()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'host.json')  # Construct the file path

# Save host data to JSON file
with open(file_path, 'w') as json_file:
    json.dump(host_data, json_file, indent=4)

print("Host data saved to 'host.json' file.")
