from .base import AuthorsBaseFunctionalTest
from time import sleep


class AuthorsRegisterFunctionalTest(AuthorsBaseFunctionalTest):
    def test_the_test(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        sleep(5)
