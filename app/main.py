from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import post_routes, register_route, auth_routes

app = FastAPI()

origins = [
    "http://localhost:8001",
    "http://127.0.0.1:8001"
]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(register_route.router)
app.include_router(auth_routes.router)
app.include_router(post_routes.router)

