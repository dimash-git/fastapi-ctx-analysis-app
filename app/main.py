from fastapi import FastAPI
from .routes import post_routes, register_route, auth_routes
from .models import user_model
from .database import engine

user_model.Base.metadata.create_all(bind=engine)
# user_model.Base.metadata.drop_all(bind=engine)

app = FastAPI()

app.include_router(post_routes.router)
app.include_router(register_route.router)
app.include_router(auth_routes.router)
