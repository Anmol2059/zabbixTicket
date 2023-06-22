import json
import os
from pyzabbix import ZabbixAPI
import datetime

zapi = ZabbixAPI('http://182.93.91.116/zabbix/')
zapi.login("Admin", "zabbix")


hosts = zapi.host.get(output=['hostid', 'name'])

problem_data = []

for host in hosts:
    host_id = host['hostid']
    host_name = host['name']

    problems = zapi.problem.get(
        output=['eventid', 'clock', 'severity', 'name', 'r_eventid', 'r_clock'],
        select_acknowledges='extend',
        select_tags='extend',
        hostids=[host_id],
        # filter={'value': 1},
        recent='true'
    )

    for problem in problems:
        problem_start_time = problem['clock']
        problem_severity = problem['severity']
        problem_description = problem['name']
        resolved_event_id = problem.get('r_eventid', '')
        resolved_time = problem.get('r_clock', '')

        # Convert UNIX timestamps to datetime objects
        start_time = datetime.datetime.fromtimestamp(int(problem_start_time)).strftime('%Y-%m-%d %H:%M:%S')
        recovery_time = datetime.datetime.fromtimestamp(int(resolved_time)).strftime('%Y-%m-%d %H:%M:%S') if resolved_time and int(resolved_time) != 0 else '-'

        status = 'Resolved' if resolved_event_id else 'Unresolved'

        problem_info = {
            'Time': start_time,
            'RTime': recovery_time,
            'Severity': problem_severity,
            'Description': problem_description,
            'Host': host_name
        }

        problem_data.append(problem_info)

problem_data.sort(key=lambda x: datetime.datetime.strptime(x['Time'], '%Y-%m-%d %H:%M:%S'), reverse=True)

zapi.user.logout()

file_path = os.path.join(os.path.dirname(__file__), 'history.json')
with open(file_path, 'w') as json_file:
    json.dump(problem_data, json_file, indent=4)

print("Problem data saved to 'history.json' file.")
