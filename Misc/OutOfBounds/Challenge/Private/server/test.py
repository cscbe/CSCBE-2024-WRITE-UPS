#!/bin/python3

import requests
from random import randint

count_success = 0
for i in range(200000):
    ip = f"10.10.10.{randint(1, 250)}"
    headers = {"X-Forwarded-For": ip}

    a = requests.get("http://localhost:3000", headers=headers)

    if a.status_code == 200:
        count_success += 1

    print(f"{count_success}/{i} Raw: {a}")
