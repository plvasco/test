import http.client
import ssl
import json, sys, argparse
import csv, requests
from datetime import datetime
import base64
"""
Run script as follows:-
python3 ops-at.py --username=admin --password=smooch1991
"""

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username",dest ="username", help="User name")
parser.add_argument("-p", "--password",dest = "password", help="Password")

args = parser.parse_args()

username=args.username
password=args.password


# Ansible tower host address.
host = "10.247.92.40"



inactive_users_list = []
inactive_users_list_fields = ['UserName']

def get_ansible_tower_version(host, token):
    conn = http.client.HTTPSConnection(
        host, context=ssl._create_unverified_context())
    payload = ''

    url = f"https://{host}/api/v2/ping/"

    headers = {'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'}

    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
        data = response.json()
        server_info = data['version']
        return server_info
    except requests.exceptions.HTTPError as errh:
        print(f"\nAn Http Error occurred: {repr(errh)}\n")
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(f"\nAn Error Connecting to the API occurred: {repr(errc)}\n")
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(f"\nA Timeout Error occurred: {repr(errt)}\n")
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(f"\nAn Unknown Error occurred: {repr(err)} \n")    
    

payload={}
headers = {
    'Content-Type': 'application/json', 
    "Authorization":"Basic {}".format(base64.b64encode(bytes(f"{username}:{password}","utf-8")).decode("ascii"))
    }

url = f"https://{host}/api/v2/tokens/"
try:
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    response.raise_for_status()
    data = response.json()
    token = data['token'].strip()  
except requests.exceptions.HTTPError as errh:
    print(f"\nAn Http Error occurred: {repr(errh)}\n")
    sys.exit(1)
except requests.exceptions.ConnectionError as errc:
    print(f"\nAn Error Connecting to the API occurred: {repr(errc)}\n")
    sys.exit(1)
except requests.exceptions.Timeout as errt:
    print(f"\nA Timeout Error occurred: {repr(errt)}\n")
    sys.exit(1)
except requests.exceptions.RequestException as err:
    print(f"\nAn Unknown Error occurred: {repr(err)} \n")


### Fetch basic information from server.
server_info=get_ansible_tower_version(host, token)
print(f"\nServer info: Ansible Tower version => {server_info}\n")

# Search for user who haven't logged in for last n days. i.e 30
days_before_marked_inactive = 30

# Get users list.

payload = ''

headers = {'Authorization': 'Bearer ' + token,
           'Content-Type': 'application/json'}

url = f"https://{host}/api/v2/users/"
try:
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as errh:
    print(f"\nAn Http Error occurred: {repr(errh)}\n")
    sys.exit(1)
except requests.exceptions.ConnectionError as errc:
    print(f"\nAn Error Connecting to the API occurred: {repr(errc)}\n")
    sys.exit(1)
except requests.exceptions.Timeout as errt:
    print(f"\nA Timeout Error occurred: {repr(errt)}\n")
    sys.exit(1)
except requests.exceptions.RequestException as err:
    print(f"\nAn Unknown Error occurred: {repr(err)} \n")


users_list = data    

print(f"Parsing response from server: \n  {users_list}.\n\n")

for user in users_list["results"]:

    login_date = str(user['last_login']).split("T")
    login_date[0] = "2022-10-03"  # Test it here.
    try:     
        dt = datetime.strptime(login_date[0], '%Y-%m-%d')
        if "None" not in login_date:
            print(f"User {user['username']} last logged in on {user['last_login']}")
        else:
            print(f"No recent Login activity from user {user['username']}")

        time_between_insertion = datetime.now() - dt

        if time_between_insertion.days > days_before_marked_inactive:
            inactive_users_list.append(user['username'])
    except ValueError as e:
        print(f"user {user['username']} hasnt logged in recently.")

print(inactive_users_list)
with open('inactive_users.csv', 'w') as f:
    w = csv.writer(f, delimiter="\n")
    w.writerow(inactive_users_list_fields)
    w.writerow(inactive_users_list)
    f.close()
