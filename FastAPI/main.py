from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()

class Products (BaseModel) :
    name: str
    description: str
    price: float

mydb = psycopg2.connect(
    host = "localhost",
    user = "postgres",
    password = "0000",
    database = "postgres"
)

cur = mydb.cursor()

@app.get("/")
def welcome_page() :
    return {"meesage":"welcome to my server this is root page"}

@app.get("/products/get")
def get_products():
    cur.execute("SELECT * FROM products")
    return cur.fetchall()

@app.post("/products/add")
def add_products(prod:Products):
    query = "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)"
    cur.execute(query, (prod.name, prod.description, prod.price))
    mydb.commit()
    return "added the products into the database"

@app.put("/products/change")
def change_products (id:int, prod:Products) :
    querry = """ 
                UPDATE products 
                SET 
                    name = %s,
                    description = %s,
                    price = %s
                WHERE id = %s
             """
    cur.execute(querry, (prod.name, prod.description, prod.price, id))
    mydb.commit()
    return {'Meassage': "updated data in database"}

@app.delete("/products/delete")
def delete_products(id:int):
    querry = """
             DELETE FROM products
             WHERE id=%s
             """
    cur.execute(querry, (id,))
    return {"Message":f"deleted the product with id = {id}"}