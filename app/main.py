from fastapi import FastAPI, Response
from app.projects.router import router as projects_router
from app.users.router import router as users_router
from app.subtasks.router import router as subtask_router
from app.tasks.router import router as task_router
from app.categories.router import router as categories_router

app = FastAPI()

app.include_router(projects_router, prefix='/api/v1')
app.include_router(users_router, prefix='/api/v1')
app.include_router(subtask_router, prefix='/api/v1')
app.include_router(task_router, prefix='/api/v1')
app.include_router(categories_router, prefix='/api/v1')

@app.get('/health')
def check_health():
    return Response(content='OK', status_code=200)

@app.get("/")
def root():
    return {"message": "Server work"}