from fastapi import FastAPI
from sqlalchemy import text
from app.config import settings
from app.database import engine, Base, AsyncSessionLocal
from contextlib import asynccontextmanager
from app.schemas import UserCreate, UserResponse
from app.api.v1 import api_router
from fastapi.middleware.cors import CORSMiddleware

# @app.on_event("startup")
# async def startup():
#     "Runs when the application start"
#     #Crea las tablas en la BD
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     print("Connected Database")
#
# @app.on_event("shutdown")
# async def shutdown():
#     """Runs when the application shuts down"""
#     await engine.dispose()
#     print("Disconnected Database")

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Startup: run on start
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Connected DataBase")

    yield # Run Application

    #Shutdown: run on close
    await engine.dispose()
    print("Disconnected DataBase")

app = FastAPI(
    title=settings.APP_NAME,
    description="Sistema API Backend",
    version="0.1.0",
    lifespan=lifespan,
)

#Middleware
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:5173"],  # tu frontend
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Register routers
app.include_router(api_router)

@app.get("/")
async def root():
    """Test Endpoint"""
    return {
        "mensaje": "API Documentation",
        "version": "0.1.0",
        "status": "READY"
    }

@app.get("/health")
async def health_check():
    """Verify that the API is working"""
    return {"status": "OK"}

@app.get("/db-test")
async def test_db():
    """Test DB conecction"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("select version();"))
            version = result.scalar()

            return {
                "status": "OK",
                "postgresql_version": version
            }
    except Exception as e:
        return {
            "status": "ERROR",
            "detalle": str(e)
        }

@app.get("/users")
async def get_users():
    return {"status": "OK"}

@app.post("/test-schema", response_model=UserResponse)
async def test_schema(user_data: UserCreate):
    """Endpoint temporal para probar schemas."""
    # Simula una respuesta (sin guardar en BD aún)
    return {
        "id": 1,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "role": user_data.role,
        "is_active": True,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }