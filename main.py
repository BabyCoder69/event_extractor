import pdfplumber
from datetime import time
from openai_utils import *
import pandas as pd
import docx


# Extract tables from the PDF
def extract_tables_from_pdf(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract tables from each page
            tables_on_page = page.extract_tables()
            if tables_on_page:
                tables.extend(tables_on_page)
    return tables


def process_pdf(pdf_path):
    # Extract the tables from the provided PDF
    extracted_tables = extract_tables_from_pdf(pdf_path)

    events = []
    for table in extracted_tables:
        data = extract_pdf_data(table=table)
        # print(f"Extracted data: {data['data']}")
        events.extend(data["data"])

    return {
        "status": "SUCCESS",
        "message": "Successfully created Agenda",
        "events": events
    }


def custom_converter(o):
    if isinstance(o, time):
        return o.strftime('%H:%M')  # Convert time to string
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


def process_xlsx(file_path):
    df = pd.DataFrame(pd.read_excel(file_path))

    # Iterate over the rows and convert each row to a dictionary
    json_objects = []
    for _, row in df.iterrows():
        # Convert the row to a dictionary, with keys as the column headers
        row_dict = row.to_dict()

        # Convert the dictionary to a JSON object (string format)
        json_object = json.dumps(row_dict, default=custom_converter)

        # Append the JSON object to the list
        json_objects.append(json_object)

    events = []
    for start in range(0, len(json_objects), 10):
        chunk = json_objects[start:start + 10]

        data = extract_xlsx_data(chunk)
        events.extend(data["data"])

    return {
        "status": "SUCCESS",
        "message": "Successfully created Agenda",
        "events": events
    }


def extract_tables_from_docx(file_path):
    doc = docx.Document(file_path)
    all_tables_data = []

    # Iterate over all tables in the document
    for table in doc.tables:
        table_data = []  # Store data for the current table

        # Extract headers (assumed to be in the first row of the table)
        headers = [cell.text.strip() for cell in table.rows[0].cells]

        # Iterate over the remaining rows
        for row in table.rows[1:]:
            row_data = {}
            for i, cell in enumerate(row.cells):
                row_data[headers[i]] = cell.text.strip()

            # Append the row data to the current table data
            table_data.append(row_data)

        # Append the current table to the overall list of tables
        all_tables_data.append(table_data)

    return all_tables_data





def process_docx(file_path):
    # Extract the tables and convert to JSON objects
    tables_json = extract_tables_from_docx(file_path)
    events = []
    # Print the JSON objects in chunks of 10
    for json_objects in tables_json:

        for start in range(0, len(json_objects), 10):
            chunk = json_objects[start:start + 10]
            data = extract_docx_data(chunk)
            events.extend(data["data"])

    return {
        "status": "SUCCESS",
        "message": "Successfully created Agenda",
        "events": events
    }


if __name__ == "__main__":
    # file_path = "/Users/haricharan/Documents/desktop-old/Personal/Inter prep/projects/drive-download-20241008T130554Z-001/RFP1.pdf"
    # file_path = "/Users/haricharan/Documents/desktop-old/Personal/Inter prep/projects/drive-download-20241008T130554Z-001/RFP2.xlsx"
    file_path = "/Users/haricharan/Documents/desktop-old/Personal/Inter prep/projects/drive-download-20241008T130554Z-001/RFP3.docx"

    if file_path.endswith(".pdf"):
        result = process_pdf(file_path)
    elif file_path.endswith(".xlsx"):
        result = process_xlsx(file_path)
    elif file_path.endswith(".docx"):
        result = process_docx(file_path)

    output_file = file_path.split("/")[-1].split(".")[0]

    with open(f"{output_file}_output.json", "w") as f:
        json.dump(result, f, indent=4)
