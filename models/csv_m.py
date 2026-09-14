from pydantic import BaseModel

class CSV_text_input(BaseModel):
    headers: list[str]
    lines: list

class CSV(BaseModel):
    csv_text: CSV_text_input
