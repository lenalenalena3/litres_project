from typing import Optional


class Book:
    def __init__(self,
                 name: Optional[str] = None,
                 author: Optional[str] = None,
                 price: Optional[str] = None,
                 id: Optional[str] = None):
        self.name = name
        self.author = author
        self.price = price
        self.id = id

    def __hash__(self):
        return hash((self.name, self.author))

    def __repr__(self):
        return f"Book(name='{self.name}', author='{self.author}', price='{self.price}', id='{self.id}')"

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return self.name == other.name and self.author == other.author

    def equals_by_id(self, other):
        if not isinstance(other, Book):
            return False
        return self.id == other.id

    def equals_by_name(self, other):
        if not isinstance(other, Book):
            return False
        return self.name == other.name