from typing import Protocol, Optional
from datetime import datetime

import requests
import pydantic


from src.config import (
    SEA_TABLE_USERNAME,
    SEA_TABLE_PASSWORD,
    SEA_TABLE_DB_NAME,
    SEA_TABLE_WORKSPACE_ID,
    SEA_TABLE_API_TOKEN,
)


class Model(Protocol):
    pass


class RowModel(pydantic.BaseModel):
    id: Optional[str] = pydantic.Field(alias='_id')
    title: Optional[str]
    data: Optional[str]
    mtime: Optional[str] = pydantic.Field(alias='_mtime')
    ctime: Optional[str] = pydantic.Field(alias='_ctime')


class SeaTableModel:
    def __init__(self, username: str, password: str):
        self._api_token = self._get_api_token(username, password)
        self._base_token = None

        self._table_name = None
        self._base_uuid = None

    @staticmethod
    def _get_api_token(username: str, password: str):
        assert username, "SeaTableModel: _get_api_token: username was not supplied"
        assert password, "SeaTableModel: _get_api_token: password was not supplied"

        # url = "https://cloud.seatable.io/api2/auth-token/"
        # body = {
        #     "username": username,
        #     "password": password,
        # }
        # r = requests.post(url, json=body)
        # if not r.ok:
        #     raise Exception("Could not get token")
        #
        # return r.json()["token"]
        return SEA_TABLE_API_TOKEN

    def get_base_token(self, db_name, workspace_id) -> dict:
        assert self._api_token,  "SeaTableModel: _get_base_token: _api_token was not supplied"
        assert db_name,  "SeaTableModel: _get_base_token: db_name was not supplied"
        assert workspace_id,  "SeaTableModel: _get_base_token: workspace_id was not supplied"

        url = f"https://cloud.seatable.io/api/v2.1/dtable/app-access-token/"
        headers = {
            "Accept": "application/json; indent=4",
            "Authorization": f"Token {self._api_token}"
        }
        r = requests.get(url, headers=headers)

        if not r.ok:
            raise Exception(f"SeaTableModel: _get_base_token: Could not get base token: {r.status_code}: {r.content}")
        
        response = r.json()

        self._base_token = response["access_token"]
        self._base_uuid = response["dtable_uuid"]

        return response

    def read_all_rows(self, table_name, view_name='Default View') -> list[RowModel]:
        url = f"https://cloud.seatable.io/dtable-server/api/v1/dtables/{self._base_uuid}/rows/?table_name={table_name}&table_view={view_name}"
        headers = {
            "Authorization": f"Token {self._base_token}",
            "Accept": "application/json; indent=4",
        }
        r = requests.get(url, headers=headers)
        if not r.ok:
            raise Exception(f"Could not get list of columns: {r.status_code}: {r.content}")

        return r.json()['rows']

    def create_row(self, table_name, row: RowModel):
        url = f"https://cloud.seatable.io/dtable-server/api/v1/dtables/{self._base_uuid}/rows/"
        headers = {
            "Authorization": f"Token {self._base_token}",
            "Accept": "application/json; indent=4",
        }
        body = {
            "table_name": table_name,
            "row": row.dict()
        }
        r = requests.post(url, headers=headers, json=body)
        if not r.ok:
            raise Exception(f"Could not get list of columns: {r.status_code}: {r.content}")

        return r.json()

    def update_row(self, table_name, row: RowModel):
        url = f"https://cloud.seatable.io/dtable-server/api/v1/dtables/{self._base_uuid}/rows/"
        headers = {
            "Authorization": f"Token {self._base_token}",
            "Accept": "application/json; indent=4",
        }
        body = {
            "table_name": table_name,
            "row": row.dict(exclude_unset=True),
            "row_id": row.id,
        }
        r = requests.put(url, headers=headers, json=body)
        if not r.ok:
            raise Exception(f"Could not update row: {r.status_code}: {r.content}")

        return r.json()

    def delete_row(self, table_name, row_id: str):
        url = f"https://cloud.seatable.io/dtable-server/api/v1/dtables/{self._base_uuid}/rows/"
        headers = {
            "Authorization": f"Token {self._base_token}",
            "Accept": "application/json; indent=4",
        }
        body = {
            "table_name": table_name,
            "row_id": row_id,
        }
        r = requests.delete(url, headers=headers, json=body)
        if not r.ok:
            raise Exception(f"Could not update row: {r.status_code}: {r.content}")

        return r.json()


model = SeaTableModel(username=SEA_TABLE_USERNAME, password=SEA_TABLE_PASSWORD)
model.get_base_token(db_name=SEA_TABLE_DB_NAME, workspace_id=SEA_TABLE_WORKSPACE_ID)
