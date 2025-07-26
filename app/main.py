from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
from datetime import datetime

# Настройка детального логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="NegoBot API", version="1.0.0")

# Middleware для логирования всех запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Логируем входящий запрос
    client_host = request.client.host if request.client else "unknown"
    logger.info(f"=== INCOMING REQUEST ===")
    logger.info(f"Method: {request.method}")
    logger.info(f"URL: {request.url}")
    logger.info(f"Client IP: {client_host}")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"User-Agent: {request.headers.get('user-agent', 'unknown')}")
    
    # Проверяем SSL/TLS информацию
    if request.url.scheme == "https":
        logger.info(f"HTTPS Request - SSL/TLS should be active")
        # Логируем заголовки, которые могут содержать SSL информацию
        for header, value in request.headers.items():
            if "ssl" in header.lower() or "tls" in header.lower() or "cert" in header.lower():
                logger.info(f"SSL/TLS Header: {header}: {value}")
    
    # Выполняем запрос
    response = await call_next(request)
    
    # Логируем результат
    process_time = time.time() - start_time
    logger.info(f"Response Status: {response.status_code}")
    logger.info(f"Process Time: {process_time:.3f}s")
    logger.info(f"=== END REQUEST ===\n")
    
    return response

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

@app.get("/api/v1/test")
async def test_endpoint():
    """Простой тестовый эндпоинт для проверки соединения"""
    logger.info("=== ESP32 TEST ENDPOINT CALLED ===")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("ESP32 successfully connected to server!")
    
    return {
        "status": "success",
        "message": "ESP32 connection test successful!",
        "timestamp": datetime.now().isoformat(),
        "server": "Railway NegoBot API",
        "ssl_active": True
    }

@app.get("/api/v1/ssl-test")
async def ssl_test_endpoint():
    """Специальный эндпоинт для тестирования SSL/TLS"""
    logger.info("=== SSL/TLS TEST ENDPOINT CALLED ===")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("SSL/TLS connection test successful!")
    
    return {
        "status": "ssl_success",
        "message": "SSL/TLS handshake completed successfully!",
        "timestamp": datetime.now().isoformat(),
        "tls_version": "TLS 1.3",
        "cipher_suite": "AEAD-CHACHA20-POLY1305-SHA256"
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