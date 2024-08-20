from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class EnvironmentData(BaseModel):
    temperature: float
    humidity: float


@app.post("/")
def receive_environment_data(data: EnvironmentData):
    # Processamento dos dados pode ser feito aqui
    return {
        "message": "Dados recebidos com sucesso!",
        "temperature": data.temperature,
        "humidity": data.humidity,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.234.185", port=8000, reload=True)
