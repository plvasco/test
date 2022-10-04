import http.client
import ssl
import json, sys
import csv
from datetime import datetime

# Ansible tower host address.
host = "35.170.182.33:8043"

# Awx tower api access token.
token = "YvlxcFj2dTsRkK8fORtd7cfGctQgUn"

inactive_users_list = []
inactive_users_list_fields = ['UserName']

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