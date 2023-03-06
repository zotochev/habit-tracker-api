from typing import Optional

import pydantic

from src.app import app, model
from src.models.model import RowModel


@app.get("/")
def read_root():
    return {"Hello": "World1"}


@app.get("/api/v1/rows")
def read_rows() -> list[RowModel]:
    return model.read_all_rows(table_name="Table1")


@app.post("/api/v1/row")
def create_row(row: RowModel) -> RowModel:
    return model.create_row(table_name="Table1", row=row)


@app.put("/api/v1/row")
def update_row(row: RowModel) -> dict:
    return model.update_row(table_name="Table1", row=row)


@app.delete("/api/v1/row")
def delete_row(row_id: str) -> dict:
    return model.delete_row(table_name="Table1", row_id=row_id)


# TEMP FOR TESTING


@app.get("/api/v1/row/delete-query")
def delete_row_get(_id: str) -> dict:
    return model.delete_row(table_name="Table1", row_id=_id)


@app.get("/api/v1/row/update-query")
def update_row_query(_id: str, title: Optional[str], data: Optional[str]) -> dict:
    row = RowModel(_id=_id, title=title, data=data)
    return model.update_row(table_name="Table1", row=row)


@app.get("/api/v1/row/test")
def create_row_test() -> RowModel:
    row = RowModel(title="qwerty", data="foobar")
    return model.create_row(table_name="Table1", row=row)
