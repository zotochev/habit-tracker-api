import os

import logging

from dotenv import load_dotenv


load_dotenv()

# SeaTable
SEA_TABLE_USERNAME = os.getenv("SEA_TABLE_USERNAME")
SEA_TABLE_PASSWORD = os.getenv("SEA_TABLE_PASSWORD")
SEA_TABLE_API_TOKEN = os.getenv("SEA_TABLE_API_TOKEN")

assert SEA_TABLE_USERNAME, "Config: SEA_TABLE_USERNAME was not supplied"
assert SEA_TABLE_PASSWORD, "Config: SEA_TABLE_PASSWORD was not supplied"
assert SEA_TABLE_API_TOKEN, "Config: SEA_TABLE_API_TOKEN was not supplied"
# --env VAR1=value1

SEA_TABLE_DB_NAME = "first-sea-base"
SEA_TABLE_WORKSPACE_ID = 32641
