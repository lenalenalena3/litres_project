import allure

from litres_project.models.book_model import Book
from litres_project.utils.logging import book_attaching


def extract_book_id(url):
    if not url:
        return None
    parts = url.rstrip('/').split('-')

    last_part = parts[-1]
    digits = ''.join(c for c in last_part if c.isdigit())

    return digits if digits else None


@allure.step("Проверить, что в полученном json содержится текст: {text}")
def verify_response_text(json_text, text):
    word_lower = text.lower()
    for item in json_text["payload"]["data"]:
        text_lower = item["text"].lower()
        if word_lower not in text_lower:
            print(f'Не содержит "{text}": "{item["text"]}"')
            return False
    print(f'Все тексты содержат слово "{text}"')
    return True

def create_books(book_ids):
    books = []
    for i, book_id in enumerate(book_ids, 1):
        book = Book(id=book_id)
        book_attaching(book, f"Book{i}")
        books.append(book)
    return books