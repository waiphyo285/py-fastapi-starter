from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get_by_id(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, obj_in: CreateSchemaType):
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id: int, obj_in: CreateSchemaType):
        db_obj = self.get_by_id(db, id)
        if db_obj:
            for key, value in obj_in.model_dump().items():
                setattr(db_obj, key, value)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        db_obj = self.get_by_id(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj
