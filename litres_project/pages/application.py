from litres_project.pages.web.cart_page import CartPage
from litres_project.pages.web.favorite_page import FavoritePage
from litres_project.pages.web.list_results_page import ListResultsPage
from litres_project.pages.web.menu_page import MenuPage


class Application:
    def __init__(self):
        self.menu_page = MenuPage()
        self.favorite_page = FavoritePage()
        self.cart_page = CartPage()
        self.list_results_page = ListResultsPage()


app = Application()