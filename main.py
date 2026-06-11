from fastapi import FastAPI,Request
from routers import auth,books,users
import time
import logging
from core import settings



logger=logging.getlogger("uvicorn.access")


app=FastAPI(titles="Book Tracker API",
version="1.0.0")

app.include_router(auth.router)
app.include_router(books.router)

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