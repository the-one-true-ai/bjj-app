from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

logger = logging.getLogger("uvicorn.access")
logger.disabled = True

def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        
        # Handle preflight requests manually to prevent 405 errors
        if request.method == "OPTIONS":
            return Response(
                status_code=status.HTTP_200_OK,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, GET, OPTIONS, PUT, DELETE",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",
                },
            )

        response = await call_next(request)
        processing_time = time.time() - start_time

        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time}s"
        print(message)
        
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://sick-bjj-app.onrender.com", "http://localhost", "http://127.0.0.1", "http://localhost:5173", "http://localhost:8000", "https://bjj-app-frontend.vercel.app"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "sick-bjj-app.onrender.com"],
    )
