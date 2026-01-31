from bson import ObjectId
from typing import Type, TypeVar, Generic
from pymongo.collection import Collection
from dataclasses import asdict, is_dataclass

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, collection: Collection, model: Type[T]):
        self.collection = collection
        self.model = model

    def _to_mongo(self, obj: T) -> dict:
        if not is_dataclass(obj):
            raise TypeError("Repository supports only dataclass domain models")

        data = asdict(obj)
        if "id" in data:
            data["_id"] = data.pop("id")

        return data

    def _from_mongo(self, data: dict) -> T:
        data = data.copy()
        if "_id" in data:
            data["id"] = data.pop("_id")

        return self.model(**data)

    def insert(self, obj: T) -> T:
        data = self._to_mongo(obj)
        result = self.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return self._from_mongo(data)

    def get_by_id(self, Id: ObjectId) -> T | None:
        if not (data := self.collection.find_one({"_id": Id})):
            return None
        return self._from_mongo(data)

    def find_all(self, skip: int = 0, limit: int = 1000) -> list[T]:
        Filter = self.collection.find().skip(skip).limit(limit)
        return [self._from_mongo(data) for data in Filter]

    def delete(self, Id: ObjectId) -> bool:
        return self.collection.delete_one({"_id": Id}).deleted_count > 0

    def update(self, Id: ObjectId, **fields) -> T | None:
        if not (data := self.collection.find_one({"_id": Id})):
            return None

        updated = {**data, **{k: v for k, v in fields.items() if v is not None}}
        self.collection.replace_one({"_id": Id}, updated)
        return self._from_mongo(updated)
