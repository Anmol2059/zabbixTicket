import requests
import shutil

# Zabbix API configuration
zabbix_url = 'http://localhost/zabbix/api_jsonrpc.php'
zabbix_username = 'Admin'
zabbix_password = 'zabbix'


# Map ID of the desired map image
map_id = 1

# Additional parameters
severity_min = 0

# Zabbix API authentication
auth_payload = {
    'jsonrpc': '2.0',
    'method': 'user.login',
    'params': {
        'user': zabbix_username,
        'password': zabbix_password
    },
    'id': 1
}
auth_response = requests.post(zabbix_url, json=auth_payload)
auth_result = auth_response.json()
auth_token = auth_result['result']

# Construct map image URL
map_image_url = f'{zabbix_url}?action=map.view&sysmapid={map_id}&severity_min={severity_min}&auth={auth_token}'

# Download the map image
response = requests.get(map_image_url, stream=True)
if response.status_code == 200:
    with open('zabbix_map_image.png', 'wb') as file:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, file)
    print('Map image downloaded successfully.')
else:
    print('Failed to download the map image.')
