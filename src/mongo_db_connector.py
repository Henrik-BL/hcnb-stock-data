from pymongo import MongoClient
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List


class MongoDBConnector:
    def __init__(self, uri="mongodb://localhost:27017", db_name="hcnb_stock_data"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def _get_collection(self, collection_name: str):
        return self.db[collection_name]

    def insert_one(self, collection_name: str, data: Dict[str, Any]):
        now = datetime.now(timezone.utc)
        document = {
            **data,
            "updated_at": now
        }
        collection = self._get_collection(collection_name)
        collection.insert_one(document)

    def insert_or_replace(self, collection_name: str, query: Dict[str, Any], data: Dict[str, Any]):
        collection = self._get_collection(collection_name)
        now = datetime.now(timezone.utc)

        replacement_doc = {
            **data,
            "updated_at": now
        }
        collection.replace_one(filter=query, replacement=replacement_doc, upsert=True)

    def insert_if_not_exists(self, collection_n: str, query: Dict[str, Any], data: Dict[str, Any]):
        collection = self._get_collection(collection_n)

        existing = collection.find_one(query)
        if existing:
            return

        now = datetime.now(timezone.utc)
        document = {
            **data,
            "updated_at": now
        }

        collection.insert_one(document)

    def fetch_one(self, collection_name: str, query: Dict[str, Any],
                  projection: Optional[Dict[str, int]] = None) -> Optional[Dict[str, Any]]:
        collection = self._get_collection(collection_name)
        return collection.find_one(filter=query, projection=projection)

    def fetch_many(self, collection_name: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        collection = self._get_collection(collection_name)
        cursor = collection.find(filter=query)
        return list(cursor)
