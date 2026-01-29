from bson import ObjectId
from pydantic import BaseModel
from typing import Type, TypeVar, Generic
from pymongo.collection import Collection

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, collection: Collection, model: Type[T]):
        self.collection = collection
        self.model = model

    def insert(self, obj: T) -> T:
        data = obj.model_dump(exclude_unset=True)
        result = self.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return self.model(**data)

    def get_by_id(self, Id: str | ObjectId) -> T | None:
        if isinstance(Id, str):
            Id = ObjectId(Id)
        data = self.collection.find_one({"_id": Id})
        return self.model(**data) if data else None

    def find_all(self) -> list[T]:
        result = self.collection.find()
        return [self.model(**data) for data in result]

    def delete(self, Id: str | ObjectId) -> None:
        if isinstance(Id, str):
            Id = ObjectId(Id)
        self.collection.delete_one({"_id": Id})

    def update(self, Id: str | ObjectId, **fields) -> T | None:
        set = {k: v for k, v in fields.items() if v is not None}
        if not set:
            return self.get_by_id(Id)
        if isinstance(Id, str):
            Id = ObjectId(Id)
        data = self.collection.find_one_and_update(
            {"_id": Id},
            {"$set": set},
            return_dataument=True
        )
        return self.model(**data) if data else None
