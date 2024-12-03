import json
import os
from datetime import datetime
from typing import  Dict

def is_not_future_date(date_string: str) -> bool:
    """
    Check if a date string in yyyy-MM-dd format is not greater than today's date.
    """
    try:
        input_date = datetime.strptime(date_string, '%Y-%m-%d').date()
        today = datetime.now().date()
        
        # Return True if input_date is not greater than today
        return input_date <= today
        
    except ValueError as e:
        raise ValueError(f"Invalid date format. Please use yyyy-MM-dd format. Error: {str(e)}")

def write_json_to_file(json_data: Dict) -> None:

    """
    Writes json data to a JSON file in the '/opt/temp/' directory.
    """
    comp = json_data["competition"]["code"]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{comp}_data_{timestamp}.json'

    directory = '/opt/temp/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    try:
        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
            
        return filename

    except IOError as e:
        raise IOError(f"Error writing to file {filename}: {str(e)}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error serializing JSON: {str(e)}", e.doc, e.pos)