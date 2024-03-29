from utils.browser import make_chrome_browser
from time import sleep
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        self.browser.get(self.live_server_url)
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        sleep(seconds)
