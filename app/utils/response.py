from fastapi.responses import JSONResponse

def respond(success: bool, data=None, error=None, status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": success,
            "data": data if success else None,
            "error": error if not success else None,
        },
    )

def respond_ok(data=None):
    return respond(True, data=data, status_code=200)

def respond_created(data=None):
    return respond(True, data=data, status_code=201)

def respond_error(error=None, status_code: int = 400):
    return respond(False, error=error, status_code=status_code)
