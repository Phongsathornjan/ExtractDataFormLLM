import json

def extract_JSON(input_str):
    try:
        start_index = input_str.find('{')
        end_index = input_str.rfind('}') + 1
        json_string = input_str[start_index:end_index]
    except Exception as e:
        print(e)
        return None
    
    return json.loads(json_string)