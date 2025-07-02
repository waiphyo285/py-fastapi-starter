from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type

from pydantic import BaseModel
from app.databases.schemas.book import BookCreate, BookRead
from app.databases.tenants.resolver import get_db
from app.services.auth.dependency import jwt_required

ServiceType = TypeVar("ServiceType")
ReadSchemaType = TypeVar("ReadSchemaType", bound=BookRead)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BookCreate)

class BaseController(Generic[CreateSchemaType, ReadSchemaType]):
    def __init__(self, service: ServiceType, read_schema: Type[ReadSchemaType], create_schema: Type[CreateSchemaType]):
        self.service = service
        self.read_schema = read_schema
        self.create_schema = create_schema

    def get_router(self, prefix: str = "", tags: list[str] = None) -> APIRouter:
        router = APIRouter(
            prefix=prefix,
            tags=tags or [prefix.strip("/")],
            dependencies=[Depends(jwt_required)]
        )

        @router.get("", response_model=list[self.read_schema])
        def list_all(db: Session = Depends(get_db)):
            return self.service.get_all(db)

        @router.get("/{id}", response_model=self.read_schema)
        def get_by_id(id: int, db: Session = Depends(get_db)):
            item = self.service.get_by_id(db, id)
            if not item:
                raise HTTPException(status_code=404, detail="Not found")
            return item
        
        @router.post("", response_model=self.read_schema, status_code=201)
        def create(data: self.create_schema, db: Session = Depends(get_db)): # type: ignore
            return self.service.create(db, data)

        @router.patch("/{id}", response_model=self.read_schema)
        def update(id: int, data: self.create_schema, db: Session = Depends(get_db)): # type: ignore
            item = self.service.update(db, id, data)
            if not item:
                raise HTTPException(status_code=404, detail="Not found")
            return item

        @router.delete("/{id}", response_model=self.read_schema)
        def delete(id: int, db: Session = Depends(get_db)):
            item = self.service.delete(db, id)
            if not item:
                raise HTTPException(status_code=404, detail="Not found")
            return item

        return router
