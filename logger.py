import requests
from loguru import logger
import os
from settings import log_settings
from settings import bot_settings

logger.remove()

os.makedirs(log_settings.LOG_DIR, exist_ok=True) # создание папки, если ее нет
  
# логирование с ротацией
logger.add(
    os.path.join(log_settings.LOG_DIR, "api_log_{time}.log"),  # файл с датой
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message} in {file}: {line}", 
    level=log_settings.LEVEL,
    rotation=log_settings.ROTATION,
    compression="zip",  
    backtrace=False, 
    diagnose=False  
)

def send_log(text):
    url = f"https://api.telegram.org/bot{bot_settings.TOKEN}/sendMessage"
    
    params = {
        "chat_id": bot_settings.USER_ID,
        "text": "#прод_ad " + text,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=params)
        response.raise_for_status() 
        
        if response.json().get("ok"):
            print("Сообщение успешно отправлено")
        else:
            print("Ошибка при отправке:", response.json())
    
    except requests.exceptions.RequestException as e:
        print("Ошибка запроса:", e)
    except Exception as e:
        print("Неизвестная ошибка:", e)


def filter_logs(text):
    if text['level'].name == "ERROR":
        send_log(text['message'])
    return True
    
logger.add(lambda message: filter_logs(message.record), format="{time} {level} {message}", level="ERROR")


# экспорт логгера для использования в других файлах
def get_logger():
    logger.info("api начала свою работу")
    #logger.add(error_function, filter=lambda r: r["level"].name == "ERROR")
    return logger

logger = get_logger()