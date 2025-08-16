from litres_project.pages.web.cart_page import CartPage
from litres_project.pages.web.favorite_page import FavoritePage
from litres_project.pages.web.book_page import BookPage
from litres_project.pages.web.search_page import SearchPage
from litres_project.pages.web.menu_page import MenuPage


class Application:
    def __init__(self):
        self.menu_page = MenuPage()
        self.favorite_page = FavoritePage()
        self.cart_page = CartPage()
        self.search_page = SearchPage()
        self.book_page = BookPage()


app = Application()