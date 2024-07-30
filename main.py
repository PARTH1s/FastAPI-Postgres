# from fastapi import FastAPI, Depends, HTTPException, Path
# from sqlalchemy.orm import Session
# from database import engine, SessionLocal, Base
# from models import Table1
# import crud
# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from starlette.responses import Response
# import logging
# from starlette.middleware.cors import CORSMiddleware
# from starlette.middleware.gzip import GZipMiddleware

# # Initialize FastAPI application
# app = FastAPI()

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Define custom logging middleware
# class CustomLoggingMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         logging.info(f"Request: {request.method} {request.url}")
#         response = await call_next(request)
#         logging.info(f"Response status code: {response.status_code}")
#         return response

# # Add middleware to the application
# app.add_middleware(CustomLoggingMiddleware)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust as needed
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all HTTP methods
#     allow_headers=["*"],  # Allows all headers
# )
# app.add_middleware(GZipMiddleware)

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/")
# def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items

# @app.post("/items/")
# def create_item(name: str, value: str, db: Session = Depends(get_db)):
#     item = crud.create_item(db, name=name, value=value)
#     return item

# @app.patch("/items/{item_id}")
# def update_item(item_id: int, name: str, value: str, db: Session = Depends(get_db)):
#     item = crud.update_item(db, item_id=item_id, name=name, value=value)
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item

# @app.delete("/items/{item_id}")
# def delete_item(item_id: int, db: Session = Depends(get_db)):
#     item = crud.delete_item(db, item_id=item_id)
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"detail": "Item deleted successfully"}

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
from schemas import ItemCreate, ItemAddOrUpdate, ItemDelete, ItemUpdate, ItemResponse
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        crud.call_insert_item_procedure(db, item.name, item.value)
        return {"detail": "Item inserted successfully"}
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/items/add_or_update/")
def add_or_update_item(item: ItemAddOrUpdate, db: Session = Depends(get_db)):
    try:
        crud.call_add_or_update_item_procedure(db, item.id, item.name, item.value)
        return {"detail": "Item added or updated successfully"}
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.put("/items/update/")
def update_item(item: ItemUpdate, db: Session = Depends(get_db)):
    try:
        crud.call_update_item_procedure(db, item.id, item.name, item.value)
        return {"detail": "Item updated successfully"}
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.delete("/items/")
def delete_item(item: ItemDelete, db: Session = Depends(get_db)):
    try:
        crud.call_delete_item_procedure(db, item.id)
        return {"detail": "Item deleted successfully"}
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    try:
        item = crud.call_get_item_procedure(db, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app"}
