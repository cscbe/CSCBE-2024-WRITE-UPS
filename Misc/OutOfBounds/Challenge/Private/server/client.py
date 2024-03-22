
import requests
from random import randint

count_success = 0

a = requests.get("http://localhost:3000", headers=headers)

if a.status_code == 200:
    count_success += 1

print(f"{count_success}/{i} Raw: {a}")
