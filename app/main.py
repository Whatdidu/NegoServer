from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NegoBot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting NegoBot API server")

@app.get("/")
async def root():
    return {
        "message": "Welcome to NegoBot API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "negobot-api"
    }

@app.post("/api/v1/stt")
async def speech_to_text(request: Request):
    """Приём аудио от ESP32 для распознавания речи"""
    try:
        # Получаем raw аудио данные
        audio_data = await request.body()
        audio_size = len(audio_data)
        
        logger.info(f"Received audio from ESP32: {audio_size} bytes")
        
        # TODO: Здесь будет обработка аудио:
        # 1. Сохранить во временный файл
        # 2. Отправить в Google Speech-to-Text
        # 3. Получить текст
        # 4. Отправить в OpenAI GPT-4
        # 5. Получить ответ
        # 6. Преобразовать в речь (TTS)
        # 7. Вернуть аудио ответа
        
        # Пока возвращаем тестовый ответ
        return {
            "status": "success",
            "audio_received": audio_size,
            "message": "Audio received successfully. STT/AI processing will be implemented soon.",
            "response_audio": None  # TODO: будет содержать аудио ответа
        }
        
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to process audio: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 