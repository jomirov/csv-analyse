from fastapi.routing import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from ..model.csv_text import csv_text
from ..dependencies import process_csv_text

router = APIRouter()

@router.post('/preview')
def analyse_csv(csv_text: csv_text):
    if len(csv_text.csv_text) >= 100000:
        raise HTTPException(status_code=413)
    
    res = process_csv_text(csv_text)
    status_code = res["status_code"]

    return JSONResponse(res, status_code=status_code)