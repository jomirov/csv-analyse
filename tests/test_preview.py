from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from ..app import app

client = TestClient(app)

def test_valid_csv():
    csv_text = "item_code,quantity,location;A01,19,R1;B02,1,R9"
    res = client.post('/preview', json={"csv_text": csv_text})

    res_json = res.json()

    expected_response = {"total": 3, 
                         "valid": 3, 
                         "invalid": 0}
    factual_response = {"total": res_json["total"], 
                        "valid": res_json["valid"], 
                        "invalid": res_json["invalid"]}
    assert factual_response == expected_response

def test_one_field_error():
    csv_text = "item_code,quantity,location;A01,0,R1;B02,1,R9"
    res = client.post('/preview', json={"csv_text": csv_text})
    res_json = res.json()

    expected_response = {"total": 3, 
                         "valid": 2, 
                         "invalid": 1, 
                         "status_code": 200}
    factual_Response = {"total": res_json["total"], 
                        "valid": res_json["valid"], 
                        "invalid": res_json["invalid"], 
                        "status_code": res.status_code}
    assert factual_Response == expected_response

def test_item_code_duplicate():
    csv_text = "item_code,quantity,location;A01,2,R1;A01,1,R9"
    res = client.post('/preview', json={"csv_text": csv_text})
    res_json = res.json()

    expected_response = {"total": 3, 
                         "valid": 2, 
                         "invalid": 1, 
                         "errors": [{"row": 3, "message": "item_code_duplicate"}]}
    factual_Response = {"total": res_json["total"], 
                        "valid": res_json["valid"], 
                        "invalid": res_json["invalid"], 
                        "errors": res_json["errors"]}
    assert factual_Response == expected_response

def test_invalid_header():
    csv_text = "item_odec,quantity,location;A01,2,R1;B02,1,R9"
    res = client.post('/preview', json={"csv_text": csv_text})
    res_json = res.json()

    expected_response = {"total": 3, 
                         "valid": 2, 
                         "invalid": 1, 
                         "status_code": 400}
    factual_Response = {"total": res_json["total"], 
                        "valid": res_json["valid"], 
                        "invalid": res_json["invalid"], 
                        "status_code": res.status_code}
    assert factual_Response == expected_response

def test_too_large_entity():
    csv_text = "a"*100000
    res = client.post('/preview', json={"csv_text": csv_text})

    expected_status_code = 413
    factual_status_code = res.status_code
    assert factual_status_code == expected_status_code

def test_invalid_item_code():
    csv_text = "item_code,quantity,location;../A,5,R1;B02,1,R9"
    res = client.post('/preview', json={"csv_text": csv_text})
    res_json = res.json()

    expected_response = {"total": 3, 
                         "valid": 2, 
                         "invalid": 1, 
                         "errors": [{"row": 2, "message": "item_code_invalid_character; item_code_invalid_type"}], 
                         "status_code": 200}
    factual_Response = {"total": res_json["total"], 
                        "valid": res_json["valid"], 
                        "invalid": res_json["invalid"], 
                        "errors": res_json["errors"], 
                        "status_code": res.status_code}
    assert factual_Response == expected_response