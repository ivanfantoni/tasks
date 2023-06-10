import datetime

class Todo:
    def __init__(self, id=None, object=None, task=None, date_added=None, date_completed=None, status=None, price=None, note=None):
        self.id = id if id is not None else None
        self.object = object
        self.task = task
        self.price = float(price) if price is not None else None
        self.date_added = date_added if date_added is not None else datetime.datetime.now().isoformat()
        self.date_completed = date_completed if date_completed is not None else None
        self.status = status if status is not None else 0
        self.note = note if note is not None else None

    def __repr__(self) -> str:
        return f'({self.id},{self.object},{self.task},{self.price},{self.date_added},{self.date_completed},{self.status},{self.note})'