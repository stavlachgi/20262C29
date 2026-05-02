from fastapi import FastAPI

app = FastAPI()

@app.get("/public")
def public_endpoint():
    return {"message": "This endpoint is accessible without authentication"}
