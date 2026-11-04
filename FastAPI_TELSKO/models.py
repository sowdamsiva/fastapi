from pydantic import BaseModel

class pydantic_Product(BaseModel):
    id: int
    name: str
    description: str 
    price: float 
    quantity: int 



#-----------------------id:1----------------------
# class Product:
#     def __init__(self,id: int,name:str, descriptin: str,price: float,quantity: int):
#         self.id = id
#         self.name = name
#         self.descriptin = descriptin
#         self.price = price
#         self.quantity = quantity


