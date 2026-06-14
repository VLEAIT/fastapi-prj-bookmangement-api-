from fastapi import FastAPI,Request
from routers import auth,books,users
import time
import logging
from core import settings
from fastapi.middleware.core import CORSMiddlware
from contextlib import asynccontextmanager
from routers import api_router
from middleware.logging import LoggingMiddleware


@asynccontextmanager
async def lifespan(app:FastAPI):
    logging.getLogger("uvicorn.access").info("Intialize the enviroment")
    yield
    logging.getlogger("uvicorn.access").info("cleaning up operational resources")



app=FastAPI(
    titles=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url=f"{settings.API_V1_STR}/docs" if not settings.PRODUCTION else None,
    redocs_url=f"{settings.API_V1_STR}/redocs" if not settings.PRODUCTION else None
    )



app.add_middleware(LoggingMiddleware)

if settings.ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allowed_origins=[str(origin).strip("/") for origin in settings.ALLOWED_ORIGINS],
        allowed_credentials=True,
        allow_method=["GET","POST","PUT","PATCH","DELETE","OPTIONS"],
        allow_headers=["Content-Type","Authorization","X-Request-With"],
    )

@app.middleware("http")
async def log_requests(request:Request,call_next):
    start_time = time.perf_counter()

    try:
        response=await call_next(request)
        process_time=time.perf_counter() - start_time


        logger.info(
            f"Method: {request.method} | Path: {request.url.path} | "
            f"Status: {response.status_code} | Duration: {process_time:.4f}s"
        )

        response.headers["X-Process-Time"]=f"{process_time:.4f}s"
        return response

    except Exception as e:
        process_time =time.perf_counter()-start_time
        logger.error(f"Request failed after {process_time:.4f}s | Error:{str(e)}")
        raise e

app.include_router(api_router,preflix=settings.API_V1_STR) 