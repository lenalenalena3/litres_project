from litres_project.pages.web.cart_page import CartPage
from litres_project.pages.web.favorite_page import FavoritePage
from litres_project.pages.web.info_details_page import InfoDetailsPage
from litres_project.pages.web.search_results_page import SearchResultsPage
from litres_project.pages.web.menu_page import MenuPage


class Application:
    def __init__(self):
        self.menu_page = MenuPage()
        self.favorite_page = FavoritePage()
        self.cart_page = CartPage()
        self.search_results_page = SearchResultsPage()
        self.info_details_page = InfoDetailsPage()


app = Application()