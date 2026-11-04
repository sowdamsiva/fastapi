from fastapi import FastAPI, HTTPException


app = FastAPI()

@app.get("/")
def root_url():
    return {"message":"Welcome to fastapi"}

users={
    1:{"name":"siva",
       "orders":{
           101:{"item":"laptop","amount":9999},
           102:{"item":"mouse","amount":99}
       }},
    2:{"name":"kumar",
       "orders":{
           201:{"item":"phoone","amount":9999},
           202:{"item":"charger","amount":9999}
       }}
}

@app.get("/users/{user_id}/orders/{order_id}")
def get_user(user_id:int,order_id:int):
    if user_id not in users:
        # return "User not found"
        raise HTTPException(status_code=404,detail="User not found")
    return users[user_id]['orders'][order_id]