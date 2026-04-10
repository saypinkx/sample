from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.components.base.domain.exceptions.base import BaseServiceException
from src.components.base.infra.exceptions.not_found import EntityNotFound
from src.config import VERSION, ROUTE_PREFIX
from src.infra.logging.loggers.server import ServerLogger
from fastapi import Response
import time
from src.infra.main import startup_all, shutdown_all

# API APP
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




ROUTERS = (auth_router, post_router)
for router in ROUTERS:
    app.include_router(router)


@app.on_event("startup")
async def on_startup():
    await startup_all()


@app.on_event("shutdown")
async def on_shutdown():
    await shutdown_all()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.exception_handler(EntityNotFound)
async def exception_not_found_database_handler(request, exc: EntityNotFound):
    return JSONResponse(
        status_code=404,
        content=exc.message,
    )


@app.exception_handler(BaseServiceException)
async def exception_service_handler(request, exc: BaseServiceException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.message,
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exception: Exception):
    content = await ServerLogger.log_error(
        exception=exception,
        request=request,
    )

    return JSONResponse(status_code=500, content=content)


@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    request.state.start_time = time.perf_counter()
    return await call_next(request)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    response: Response = await call_next(request)

    if response.status_code < 500:
        await ServerLogger.log_success(request, response.status_code)

    return response


@app.get(f"{ROUTE_PREFIX}/healthcheck")
async def check():
    return VERSION
