from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Product API",
    description="API with CI/CD",
    version="1.0.0"
)

# In-memory database
products = {}
next_id = 1

class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ProductResponse(Product):
    id: int

@app.get("/")
def read_root():
    return {
        "message": "Product API with CI/CD",
        "version": "1.0.0",
        "health": "/health",
        "port": 14125
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/products", response_model=List[ProductResponse])
def get_products():
    return [{"id": k, **v} for k, v in products.items()]

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product_id, **products[product_id]}

@app.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: Product):
    global next_id
    product_id = next_id
    products[product_id] = product.dict()
    next_id += 1
    return {"id": product_id, **products[product_id]}

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: Product):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    products[product_id] = product.dict()
    return {"id": product_id, **products[product_id]}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]
    return {"message": "Product deleted"}
