import os;
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId


client = AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client["your_db_name"]
task_collection = db["tasks"]

app = FastAPI()

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    task_dict = task.dict()
    await task_collection.insert_one(task_dict)
    return task

@app.get("/tasks/", response_model=List[Task])
async def get_tasks(completed: Optional[bool] = None):
    if completed is not None:
        query = {"completed": completed}
    else:
        query = {}

    tasks = await task_collection.find(query).to_list(length=100)
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    try:
        task = await task_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID")

@app.delete("/tasks/{task_id}", response_model=Task)
async def remove_task(task_id: str):
    try:
        task = await task_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        await task_collection.delete_one({"_id": ObjectId(task_id)})
        return task
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, updated_task: Task):
    try:
        task = await task_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        await task_collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": updated_task.dict(exclude_unset=True)}
            )
        task = await task_collection.find_one({"_id": ObjectId(task_id)})
        return task
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID")