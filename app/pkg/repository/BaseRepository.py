from bson import ObjectId
from pydantic import BaseModel
from pymongo import ReturnDocument
from typing import Type, TypeVar, Generic
from pymongo.collection import Collection

TCreate = TypeVar("TCreate", bound=BaseModel)
TRead = TypeVar("TRead", bound=BaseModel)

class BaseRepository(Generic[TCreate, TRead]):
    def __init__(self, collection: Collection, model: Type[TRead]):
        self.collection = collection
        self.read_model = model

    def insert(self, obj: TCreate) -> TRead:
        data = obj.model_dump(exclude_unset=True)
        result = self.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return self.read_model(**data)

    def get_by_id(self, Id: ObjectId) -> TRead | None:
        if not (data := self.collection.find_one({"_id": Id})):
            return None
        return self.read_model(**data)

    def find_all(self, skip: 1, limit: 1000) -> list[TRead]:
        result = list(self.collection.find().skip(skip).limit(limit))
        return [self.read_model(**data) for data in result]

    def delete(self, Id: ObjectId) -> bool:
        return self.collection.delete_one({"_id": Id}).deleted_count > 0

    def update(self, Id: ObjectId, **fields) -> TRead | None:
        if not (data := self.collection.find_one({"_id": Id})):
            return None

        updated = {**data, **{k: v for k, v in fields.items() if v is not None}}
        self.collection.replace_one({"_id": Id}, updated)
        return self.read_model(**updated)