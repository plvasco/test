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
host = "ec2-13-56-76-86.us-west-1.compute.amazonaws.com"



inactive_users_list = []
inactive_users_list_fields = ['UserName']

def get_access_token(host, username, password):
    conn = http.client.HTTPSConnection(host, context=ssl._create_unverified_context())


    headers = {
        'Content-Type': 'application/json', 
        "Authorization":"Basic {}".format(base64.b64encode(bytes(f"{username}:{password}","utf-8")).decode("ascii"))
        }

        
    payload = ''

    conn.request("POST", "/api/v2/tokens/", payload, headers)
    res = conn.getresponse()
    data = res.read()
    token_data = json.loads(data.decode("utf-8")) 
    return token_data['token'].strip()

try:
    # Create new api access token.
    token = get_access_token(host, username, password)
except:
    print(f"\n\n Issue creating access token from {host}/api/v2/tokens/.. Exit.")
    sys.exit(1)


# Search for user who haven't logged in for last n days. i.e 30
days_before_marked_inactive = 30

conn = http.client.HTTPSConnection(
    host, context=ssl._create_unverified_context())
payload = ''

headers = {'Authorization': 'Bearer ' + token,
           'Content-Type': 'application/json'}

try: 
    conn.request("GET", "/api/v2/users/", payload, headers)
    res = conn.getresponse()
    data = res.read()   
    print(f"\n\nConnection to {host} is SUCCESSFUL with response {res.status}.\n\n")
except:
    print(f"\n\nConnection to {host} not open. CONNECTION ERROR!!!\n\n")
    sys.exit(1)


users_list = json.loads(data.decode("utf-8"))    

print(f"Parsing response from server: \n  {users_list}.\n\n")

for user in users_list["results"]:
    print(f"User {user['username']} last logged in on {user['last_login']}")

    login_date = str(user['last_login']).split("T")
    # login_date[0] = "2022-05-04"  # Test it here.
    try:
        dt = datetime.strptime(login_date[0], '%Y-%m-%d')

        time_between_insertion = datetime.now() - dt

        if time_between_insertion.days > days_before_marked_inactive:
            inactive_users_list.append(user['username'])
    except ValueError as e:
        print("Time data 'None' does not match format '%Y-%m-%d'")
        # raise e

print(inactive_users_list)
with open('inactive_users.csv', 'w') as f:
    w = csv.writer(f, delimiter="\n")
    w.writerow(inactive_users_list_fields)
    w.writerow(inactive_users_list)
    f.close()