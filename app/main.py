from fastapi import FastAPI
from .database import Base, engine
from .routes import auth_routes, gemini_routes
from .utils.limiter import limiter
from slowapi.middleware import SlowAPIMiddleware

# Create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Gemini Proxy")

# Rate Limiting Middleware
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Routers
app.include_router(auth_routes.router)
app.include_router(gemini_routes.router)