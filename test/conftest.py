import copy

import pytest

from hcnb_stock_data.mongo_db_connector import MongoDBConnector


class FakeCollection:
    """Minimal in-memory stand-in for a pymongo collection (equality and $in queries only)."""

    def __init__(self):
        self.docs = []

    @staticmethod
    def _matches(doc, query):
        return all(
            doc.get(k) in v["$in"] if isinstance(v, dict) and "$in" in v else doc.get(k) == v
            for k, v in (query or {}).items()
        )

    def find_one(self, filter=None, projection=None):
        for doc in self.docs:
            if self._matches(doc, filter):
                return copy.deepcopy(doc)
        return None

    def find(self, filter=None):
        return [copy.deepcopy(d) for d in self.docs if self._matches(d, filter)]

    def insert_one(self, document):
        self.docs.append(copy.deepcopy(document))

    def replace_one(self, filter, replacement, upsert=False):
        for i, doc in enumerate(self.docs):
            if self._matches(doc, filter):
                self.docs[i] = copy.deepcopy(replacement)
                return
        if upsert:
            self.docs.append(copy.deepcopy(replacement))

    def update_one(self, filter, update, upsert=False):
        fields = update["$set"]
        for doc in self.docs:
            if self._matches(doc, filter):
                doc.update(copy.deepcopy(fields))
                return
        if upsert:
            self.docs.append({**filter, **copy.deepcopy(fields)})

    def distinct(self, field):
        values = []
        for doc in self.docs:
            if field in doc and doc[field] not in values:
                values.append(doc[field])
        return values


class FakeDatabase(dict):
    def __missing__(self, name):
        self[name] = FakeCollection()
        return self[name]


@pytest.fixture
def mongo():
    connector = MongoDBConnector.__new__(MongoDBConnector)
    connector.client = None
    connector.db = FakeDatabase()
    return connector
