from . import token_settings


def check_headers(headers):
    if not headers.get('Authorization'):
        return False, "1"
    if headers.get('Authorization') == token_settings.AUTH_TOKEN:
        return True, ""
    return False, "7"

def file_reader():
    lines_result = []
    try:
        with open('application/non_changed_groups.txt') as file:
            for line in file.readlines():
                lines_result.append(line.replace("\n", ""))
            
            return lines_result

    except Exception as e:
        print(f"Возникла ошибка: {e}")
        return ""
    


    
    