
"""
    Created by Hari for Result Extraction from Anylogic project
    and storing it in Oracle DB of Transfact ERP
"""
import requests

snd = requests.get('http://localhost:8080/api/chargen?losstatus=422')

print(snd.json())