import http.client
import ssl
import json
import csv
from datetime import datetime, timedelta
from dateutil import parser

  # Ansible tower host address.
HOST = "SEVER"

    # Awx tower api access token.
TOKEN = "TOKEN"


inactive_users_list = []
inactive_users_list_fields = ['UserName']

        # Search for user who haven't logged in for last n days. i.e 30
days_before_marked_inactive = 30

conn = http.client.HTTPSConnection(HOST)
payload = ''


headers = {
  'Authorization': 'Bearer 1CM6uSVwlR7bFsCrI0ZwrsdsfiS3lY',
  'Cookie': 'a240bfef5ed9b602fca9ab1d788a7bbf=681820e976dc7aab860623e6fbdc02e4; csrftoken=TOKEN'
}
conn.request("GET", "/api/v2/users", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

