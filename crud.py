# from sqlalchemy.orm import Session
# from models import Table1

# def get_item(db: Session, item_id: int):
#     return db.query(Table1).filter(Table1.id == item_id).first()

# def get_items(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(Table1).offset(skip).limit(limit).all()

# def create_item(db: Session, name: str, value: str):
#     db_item = Table1(name=name, value=value)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# def update_item(db: Session, item_id: int, name: str, value: str):
#     db_item = db.query(Table1).filter(Table1.id == item_id).first()
#     if db_item:
#         db_item.name = name
#         db_item.value = value
#         db.commit()
#         db.refresh(db_item)
#     return db_item

# def delete_item(db: Session, item_id: int):
#     db_item = db.query(Table1).filter(Table1.id == item_id).first()
#     if db_item:
#         db.delete(db_item)
#         db.commit()
#     return db_item



from sqlalchemy.orm import Session
from sqlalchemy.sql import text

def call_insert_item_procedure(db: Session, name: str, value: str):
    try:
        sql = text("SELECT insert_item(:name, :value)")
        db.execute(sql, {"name": name, "value": value})
        db.commit()
    except Exception as e:
        import logging
        logging.error("Error occurred while inserting item", exc_info=True)
        raise

def call_add_or_update_item_procedure(db: Session, item_id: int, name: str, value: str):
    try:
        sql = text("SELECT add_or_update_item(:id, :name, :value)")
        db.execute(sql, {"id": item_id, "name": name, "value": value})
        db.commit()
    except Exception as e:
        import logging
        logging.error("Error occurred while adding or updating item", exc_info=True)
        raise

def call_delete_item_procedure(db: Session, item_id: int):
    try:
        sql = text("SELECT delete_item(:id)")
        db.execute(sql, {"id": item_id})
        db.commit()
    except Exception as e:
        import logging
        logging.error("Error occurred while deleting item", exc_info=True)
        raise

def call_update_item_procedure(db: Session, item_id: int, name: str, value: str):
    try:
        sql = text("SELECT update_item(:id, :name, :value)")
        db.execute(sql, {"id": item_id, "name": name, "value": value})
        db.commit()
    except Exception as e:
        import logging
        logging.error("Error occurred while updating item", exc_info=True)
        raise

def call_get_item_procedure(db: Session, item_id: int):
    try:
        sql = text("SELECT * FROM get_item(:id)")
        result = db.execute(sql, {"id": item_id}).fetchone()
        if result:
            # Convert result to a dictionary
            return dict(result._asdict())
        return None
    except Exception as e:
        import logging
        logging.error("Error occurred while retrieving item", exc_info=True)
        raise
