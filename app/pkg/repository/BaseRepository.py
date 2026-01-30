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

    def get_by_id(self, Id: str | ObjectId) -> TRead | None:
        if isinstance(Id, str):
            Id = ObjectId(Id)
        data = self.collection.find_one({"_id": Id})
        return self.read_model(**data) if data else None

    def find_all(self) -> list[TRead]:
        return [self.read_model(**doc) for doc in self.collection.find()]

    def delete(self, Id: str | ObjectId) -> None:
        if isinstance(Id, str):
            Id = ObjectId(Id)
        self.collection.delete_one({"_id": Id})

    def update(self, Id: str | ObjectId, **fields) -> TRead | None:
        update = {k: v for k, v in fields.items() if v is not None}
        if not update:
            return self.get_by_id(Id)
        if isinstance(Id, str):
            Id = ObjectId(Id)

        data = self.collection.find_one_and_update(
            {"_id": Id},
            {"$set": update},
            return_document=ReturnDocument.AFTER
        )
        return self.read_model(**data) if data else None
