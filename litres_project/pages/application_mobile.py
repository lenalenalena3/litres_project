from litres_project.pages.mobile.book_page_mobile import BookPageMobile
from litres_project.pages.mobile.favorite_page_mobile import FavoritePageMobile
from litres_project.pages.mobile.search_page_mobile import SearchPageMobile


class Application:
    def __init__(self):
        self.book_page_mobile = BookPageMobile()
        self.search_page_mobile = SearchPageMobile()
        self.favorite_page_mobile = FavoritePageMobile()


app_mobile = Application()
