from fastapi import FastAPI, Depends
from models import pydantic_Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session


app=FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    print("Welcome to fast api")
    return "Welcome to fast api"


products = [
    pydantic_Product(id = 1,name = "Phone",description="budget phone",price=999,quantity=10),
    pydantic_Product(id = 2,name = "laptop",description="budget laptop",price=8888,quantity=2),
    pydantic_Product(id = 5,name = "TV",description="budget tv",price=2000,quantity=8)
]

def init_db():
    db = session()    

    count = db.query(database_models.Product).count()
    print("count",count)
    if count == 0:
        for product in products:
            print("dump data:",product.model_dump())
            db.add(database_models.Product(**product.model_dump()))

        db.commit()
    
init_db()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@app.get("/products")
def get_all_products(db : Session=Depends(get_db)):
    # db = session()
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int,db: Session=Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product
        
    return "Product not found"


#lets create product
@app.post("/product")
def create_product(product:pydantic_Product, db:Session=Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

#lets update
@app.put("/product")
def update_product(id: int, product:pydantic_Product,db: Session=Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
            db_product.name = product.name
            db_product.description = product.description
            db_product.quantity = product.quantity
            db.commit()
            return "Updated successfully"
    return "No product Found"


@app.delete("/product")
def delete_product(id: int,db: Session=Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
            db.delete(db_product)
            db.commit()
            return "deleted successfully"
    return "No product Found"








#-----------------------id:1----------------------
#basic learning
# @app.get("/")
# def greet():
#     print("Welcome to fast api")
#     return "Welcome to fast api"


# products = [
#     Product(id = 1,name = "Phone",description="budget phone",price=999,quantity=10),
#     Product(id = 2,name = "laptop",description="budget laptop",price=8888,quantity=2),
#     Product(id = 5,name = "TV",description="budget tv",price=2000,quantity=8)
# ]

# @app.get("/products")
# def get_all_products():
#     return products
#         if product.id == id:

# @app.get("/product/{id}")
# def get_product_by_id(id:int):
#     for product in products:
#             return product
        
#     return "Product not found"


# #lets create product
# @app.post("/product")
# def create_product(product:Product):
#     products.append(product)
#     return product

# #lets update
# @app.put("/product")
# def update_product(id: int, product:Product):
#     for i in range(len(products)):
#         if products[i].id == id:
#             products[i] = product
#             return "Updated successfully"
#     return "No product Found"


# @app.delete("/product")
# def update_product(id: int):
#     for i in range(len(products)):
#         if products[i].id == id:
#             del products[i]
#             return "deleted successfully"
#     return "No product Found"