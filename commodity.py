from mongo_db import get_document, create_document, update_document

VALID_COMMODITIES = ["BTC", "GOLD"]

class Commodity():
    def __init__(self, default_value_dict):
        self._title = default_value_dict["title"]
        self._query = {"title": self._title}
        self._data = None
        self._db_updated = False
        if self._title in VALID_COMMODITIES:
            self._get_document(default_value_dict)
    
    def _clear_db_update(self):
        self._db_updated = False

    def _db_update(self):
        self._db_updated = True

    def _is_db_updated(self):
        return self._db_updated

    def _get_document(self, default_value_dict=None):
        self._data = get_document(self._query)
        if self._data is None:
            create_document(default_value_dict)
            self._data = get_document(self._query)

    def update_percent(self, value):
        self._data["PX_OFFSET_PERCENT"] = value
        update_document(self._query, {"PX_OFFSET_PERCENT": value})
        self._db_update()

    def update_ref(self, value):
        self._data["REFERENCE"] = value
        update_document(self._query, {"REFERENCE": value})
        self._db_update()

    def _check_cache(self):
        if self._db_updated:
            self._get_document()
            self._clear_db_update()

    def get_percent(self):
        self._check_cache()
        return self._data["PX_OFFSET_PERCENT"]

    def get_ref(self):
        self._check_cache()
        return self._data["REFERENCE"]