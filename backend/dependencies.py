import csv

def add_error_details(errors: list, row: int, message: str):
    for err in errors:
        if err["row"] == row:
            err["message"] += "; " + message
            return 0
    errors.append({"row": row, "message": message})

def convert_csv_text_to_lines(csv_text):
    splitted_lines = csv_text.split(";")
    return list(csv.reader(splitted_lines))

def process_csv_text(csv_text):
    csv_reader = convert_csv_text_to_lines(csv_text.csv_text)

    errors = []
    exception_details = []

    csv_headers = csv_reader[0]
    total = len(csv_reader)
    valid = 0
    invalid = 0
    status_code = 200

    if not ("item_code" in csv_headers 
            and "quantity" in csv_headers
            and "location" in csv_headers):
        exception_details.append("invalid_header")
        invalid += 1
        status_code = 400
    else: valid += 1
    existing_item_codes = []

    i = 1
    while (i < total):
        row = i + 1
        if len(csv_reader[i]) != 3:
            i += 1
            invalid += 1
            status_code = 400
            exception_details.append("invalid_amount_of_data")
            continue            

        #item_code processing
        item_code = csv_reader[i][0].strip()

        if item_code == "":
            status_code = 400
            exception_details.append("item_code_data_is_empty")
            add_error_details(errors, row, "item_code_data_is_empty")
        elif not 97 > ord(item_code[0]) >= 65:
            add_error_details(errors, row, "item_code_invalid_character")
        elif item_code[0].upper() != item_code[0]:
            add_error_details(errors, row, "item_code_lowercase_character")
        try:
            int(item_code[1:])
            if len(item_code[1:]) != 2:
                add_error_details(errors, row, "item_code_invalid_number")
        except:
            add_error_details(errors, row, "item_code_invalid_type")
        if item_code in existing_item_codes:
            add_error_details(errors, row, "item_code_duplicate")
        existing_item_codes.append(item_code)

        #quantity processing
        quantity = csv_reader[i][1]
        try:
            if quantity == "":
                exception_details.append("quantity_data_is_empty")
                status_code = 400
            quantity = int(quantity)
            if not (20 > quantity >= 1):
                add_error_details(errors, row, "quantity_invalid_number")
        except:
            add_error_details(errors, row, "quantity_invalid_type")

        #location processing
        location = csv_reader[i][2].strip()
        if location == "":
            status_code = 400
            exception_details.append("location_data_is_empty")
            add_error_details(errors, row, "location_data_is_empty")
        elif location[0].upper() != "R":
            add_error_details(errors, row, "location_invalid_character")
        elif location[0].upper() != location[0]:
            add_error_details(errors, row, "location_lowercase_character")
        try:
            if not (9 >= int(location[1:]) >= 1):
                add_error_details(errors, row, "location_invalid_number")
        except:
            add_error_details(errors, row, "location_invalid_type")

        if len(errors) != 0 and errors[-1]["row"] == row:
            invalid += 1
        else:
            valid += 1
        i += 1

    if total > 50:
        status_code = 400
        exception_details.append("line_amount_is_more_than_fifty")

    return {"total":total, 
            "valid": valid, 
            "invalid": invalid, 
            "errors": errors, 
            "status_code": status_code,
            "details": "OK" if len(exception_details) == 0 else "; ".join(exception_details)}