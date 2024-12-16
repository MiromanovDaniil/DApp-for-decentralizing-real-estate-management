import uvicorn

# TODO implement app start up
from .base_router import app

if __name__ == "__main__":
    # app.include_router(router=test_router)
    uvicorn.run(app, host="0.0.0.0", port="8000")
