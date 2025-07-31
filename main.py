
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from endpoints.ad_api import router
from endpoints.ad_api import logger

website = FastAPI() #-> создание самой апишки

#----> обработки ошибок
@website.exception_handler(HTTPException) #-> ловит ошибочки 
async def get_http_error(request: Request, exception: HTTPException):
    logger.error('Ошибка: ' + exception)
    return JSONResponse(status_code=exception.status_code,
                        content={"error_information":{
            "message": exception
        }
    }
    )

@website.exception_handler(RequestValidationError) #-> ловит ошибку, связанную с валидацией данных
async def value_not_corrected(request: Request, exception: RequestValidationError):
    error_message = [error['msg'] for error in exception.errors()] #-> это для дальнейших ошибок
    print(exception.errors())
    logger.error(f"Ошибка под кодом 6: {error_message}")
    
    return JSONResponse({"returnCode": "6"})

if __name__ == "__main__":
    website.include_router(router)
    
    import uvicorn
    uvicorn.run(website, host="0.0.0.0", port=80)
