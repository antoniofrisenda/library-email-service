from bson import ObjectId
from dataclasses import asdict
from typing import Type, TypeVar, Generic
from pymongo.collection import Collection

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, collection: Collection, model: Type[T]) -> None:
        self.collection = collection
        self.model = model

    def _to_mongo(self, obj: T) -> dict:
        return asdict(obj)  # type: ignore

    def _from_mongo(self, data: dict) -> T:
        return self.model(**data.copy())

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
        return [self._from_mongo(data) for data in self.collection.find().skip(skip).limit(limit)]

    def delete_by_id(self, Id: ObjectId) -> bool:
        return self.collection.delete_one({"_id": Id}).deleted_count > 0

    def update_by_id(self, Id: ObjectId, **fields) -> T | None:
        if not (data := self.collection.find_one({"_id": Id})):
            return None

        updated = {**data, **{k: v for k, v in fields.items() if v is not None}}
        self.collection.replace_one({"_id": Id}, updated)
        return self._from_mongo(updated)
