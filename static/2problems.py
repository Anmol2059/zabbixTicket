import os
import json
from pyzabbix import ZabbixAPI
import datetime

# Connect to the Zabbix API
zapi = ZabbixAPI('http://182.93.91.116/zabbix/')
zapi.login("Admin", "zabbix")

# Get the hosts and their status
hosts = zapi.host.get(output=['hostid', 'name'])

problem_data = []  # Store problem data

for host in hosts:
    host_id = host['hostid']
    host_name = host['name']

    # Get problems for the host's interfaces
    problems = zapi.problem.get(
        output=['eventid', 'clock', 'severity', 'name'],
        select_acknowledges='extend',
        select_tags='extend',
        hostids=[host_id],
        filter={'value': 1}
    )

    for problem in problems:
        problem_start_time = problem['clock']
        problem_severity = problem['severity']
        problem_description = problem['name']

        # Convert UNIX timestamp to datetime object
        start_time = datetime.datetime.fromtimestamp(int(problem_start_time)).strftime('%Y-%m-%d %H:%M:%S')

        problem_info = {
            'Time': start_time,
            'Severity': problem_severity,
            'Description': problem_description,
            'Host': host_name
        }

        problem_data.append(problem_info)

# Sort problem_data based on descending time
problem_data.sort(key=lambda x: x['Time'], reverse=True)

# Disconnect from the Zabbix API
zapi.user.logout()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'problems.json')  # Construct the file path

# Save problem data to JSON file
with open(file_path, 'w') as json_file:
    json.dump(problem_data, json_file, indent=4)

print("Problem data saved to 'problems.json' file.")
