from fastapi import FastAPI, HTTPException, Request, Form, Depends

from fastapi.middleware.cors import CORSMiddleware # starlette.middleware가 fastapi.middleware 에 포함됨

from mongo_db import user_collection # sql database 에서의 session 기능과 동일함
from model import User

import uvicorn

app = FastAPI()

# 동일한 host address 에서 server기능과 client 기능이 일어남을 허용하는 middleware 임
# 실제경우는 일어나지 않으며 개발 기간동안 동일 서버 에서 개발을 허용함
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.get("/users")
async def read_users():
    users = []
    cursor = user_collection.find({})
    async for doc in cursor:
        print(doc)
        user = User(**doc)
        users.append(user)
    return users
    
@app.get("/user/{name}") # mongodb 에서는 _id 값이 objectID 로 자동 생성 되어 복잡하여 _id 값을 name 으로 대치하였음
async def read_user(name: str):
    data = {"name": name}
    # make dictionary type data for name (mongodb 에서 data 를 dict 형태로 받음)
    print(data)
    user = await user_collection.find_one(data)
    print(user)

    user = {"name": user['name'], "age": user['age']}
    # abstract name and user from dictionary to make a json file to response
    # dict 형태에서 json type 으로 바꾸어 return 함
    return (user)


@app.post("/user")
async def create_user(user:User):
    print(user)
    data = {"name": user.name, "age": user.age}
    # mongodb 에서 data 를 dict 형태로 받음
    result = await user_collection.insert_one(data)
    print(result)

    return f"{user.name} created..."


@app.delete("/user/{name}")  # mongodb 에서는 _id 값이 objectID 로 자동 생성 되어 복잡하여 _id 값을 name 으로 대치하였음
async def delete_users(name: str):
    result = await user_collection.delete_one({"name": name})
    print(result)
    return f"{result}"

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)