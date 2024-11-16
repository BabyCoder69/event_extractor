import openai
import json

opai_client = openai.OpenAI(
    api_key=""  # Please Replace with your OpenAI API key to run the code
)


def extract_pdf_data(table: list):

    res = opai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are a data extractor, your job is to parse the data and to extract all the possible 
                                json objects from the given table that fit into the given format. Pay close attention 
                                to the table to differentiate between headings and actual row data. If any field of the json object is missing, 
                                fill it with an empty string. Consider the table if only it has the following columns:
                                - Date/Time 
                                - Activity
                                - # of ppl / Set-Up
                                
                                if not return an empty list.
                                
                                The format of each json object should be as follows:
                                
                                Example:
                                    event = {
                                        "date": "",
                                        "day": Take the day from the closest row above it where only the day is mentioned in the 'Date/Time' column,
                                        "repeatCount": "",
                                        "startTime": The first time on the left in the 'Date/Time' column in the format HH:MM without am or pm,
                                        "endTime": The second time on the right in the 'Date/Time' column in the format HH:MM without am or pm,
                                        "functionType": The value in the 'Activity' column,
                                        "setupStyle": The string part of the '# of ppl/ Set-Up' column that follows the integer in the column,
                                        "peopleCount": The integer available in the '# of ppl/ Set-Up' column,
                                        "comments": ""
                                    }
                                    
                                the final result should be like this:
                                
                                {
                                    "data": list of all the json objects
                                }
                            """,
            },
            {
                "role": "user",
                "content": f"""Now extract the data from the following table: ```{table}```""",
            },
        ],
        n=1,
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    return json.loads(res.choices[0].message.content)


def extract_xlsx_data(table):
    res = opai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are a data extractor, your job is to parse the data and to extract all the possible 
                                json objects from the given table that fit into the given format. Pay close attention 
                                to the table to differentiate between headings and actual row data. If any field of the json object is missing, 
                                fill it with an empty string. 

                                The format of each json object should be as follows:

                                Example:
                                    event = {
                                        "date": "",
                                        "day": "",
                                        "repeatCount": "",
                                        "startTime": The first day in the order of (saturday, sunday, monday, tuesday, wednesday, thursday, friday) with an acceptable value other than NAN in the format HH:MM without am or pm along with the day,
                                        "endTime": The last day in the order of (saturday, sunday, monday, tuesday, wednesday, thursday, friday) with an acceptable value other than NAN in the format HH:MM without am or pm along with the day,
                                        "functionType": The value in 'Agenda Item',
                                        "setupStyle": The value in 'Room Request',
                                        "peopleCount": The integer value of the number in the 'Number of Pax' column,
                                        "comments": ""
                                    }

                                the final result should be like this:

                                {
                                    "data": list of all the json objects
                                }
                            """,
            },
            {
                "role": "user",
                "content": f"""Now extract the data from the following table: ```{table}```""",
            },
        ],
        n=1,
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    return json.loads(res.choices[0].message.content)


def extract_docx_data(table):
    res = opai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are a data extractor, your job is to parse the data and to extract all the possible 
                                json objects from the given list of json objects that fit into the given format.  
                                If any field of the json object is missing, fill it with an empty string. 
                                Consider the json object if only it has the following keys, its ok if their values are missing:
                                - Day
                                - Function
                                - Timing
                                - Set
                                - Number of attendees

                                if not do not consider that json object.

                                The format of each output json object should be as follows:

                                Example:
                                    event = {
                                        "date": "",
                                        "day": Take the 'Day' key,
                                        "repeatCount": "",
                                        "startTime": Extract from 'Timing' key, convert to 'HH:MM' format where possible,
                                        "endTime": Extract from 'Timing' key, convert to 'HH:MM' format where possible,
                                        "functionType": The value in the 'Function' key,
                                        "setupStyle": The value in the 'set' key,
                                        "peopleCount": The integer available in the 'Number of attendees' key,
                                        "comments": ""
                                    }
                                    
                                    in certain cases the time may be specified in words for example:
                                    24 hour hold, 12 hour hold, 3pm onwards etc
                                    
                                    in such cases you should convert the time to 'HH:MM' format
                                    for 24 hour hold: 
                                    - start time: 00:00
                                    - end time: 24:00
                                    for 12 hour hold:
                                    - start time: 00:00
                                    - end time: 12:00
                                    for 3pm onwards:
                                    - start time: 15:00
                                    - end time: 24:00

                                the final result should be like this:

                                {
                                    "data": list of all the json objects
                                }
                            """,
            },
            {
                "role": "user",
                "content": f"""Now extract the data from the following list of json objects: ```{table}```""",
            },
        ],
        n=1,
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    return json.loads(res.choices[0].message.content)
