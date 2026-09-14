from fastapi.routing import APIRouter
from ..models.csv_m import CSV
import sys

router = APIRouter()

@router.post('/preview', status_code=200)
def analyse_csv(c: CSV):
    print(sys.getsizeof(1))