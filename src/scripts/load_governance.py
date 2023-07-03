import json
import os

from pip._vendor.rich import print # pylint: disable=redefined-builtin

from interfaces.event import Create, Payload, Request
from interfaces.request import EventOut
from utils.taple_connector import RestConnector

with open(r'schemas/governance.json', 'r', encoding='utf-8') as file:
    governance_schema = json.load(file)
    connector = RestConnector("http://localhost",3000,"2daf002ddcf793fe73aa987fbf4aeddfca94bc89164d7a054c9bdb0b25407250")
    payload = EventOut(
        request=Request(
            create=Create(
                governance_id="",
                namespace="",
                schema_id="governance",
                payload=Payload(
                    Json=governance_schema
                )
            ),
        )
    )
    ax = connector.create_event_request(payload=payload)
    governance_id = ax.subject_id
    print(f"Governance ID: {governance_id}")

    # Atomaticly update .env file with new governance id
    enviroment = []
    if os.path.exists(".env"):
        env_file = open(".env", "r", encoding="utf-8")
        enviroment = env_file.readlines()
        env_file.close()
    env_file = open(".env", "w", encoding="utf-8")
    found = False
    for line in enviroment:
        if line.startswith("GOVERNANCE_ID"):
            found = True
            line = f"GOVERNANCE_ID={governance_id}\n"
        env_file.write(line)

    if not found:
        env_file.write(f"GOVERNANCE_ID={governance_id}\n")
    env_file.close()