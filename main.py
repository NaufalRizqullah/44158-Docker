from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from src.routers import api


app = FastAPI()

# Include all wraper router api.
app.include_router(api.main_api)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return f"Congratulations! Your API is working as expected. Now head over to <a href='{request.url}docs' target='_blank'>{request.url}docs</a>"