import json

def extract_JSON(input_str):
    start_index = input_str.find('{')
    end_index = input_str.rfind('}') + 1
    json_string = input_str[start_index:end_index]
    return json.loads(json_string)