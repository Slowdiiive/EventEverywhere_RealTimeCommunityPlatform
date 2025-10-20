from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, event, comment, like
import uvicorn

app = FastAPI(title="Event Everywhere API")

app.include_router(user.router)
app.include_router(event.router)
app.include_router(like.router)
app.include_router(comment.router)

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
