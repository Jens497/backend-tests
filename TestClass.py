import time
import traceback
import unittest
from FileLogger import FileLogging
import sys
from HttpHelpers import HttpCommandHelpers
import http.client as httplib


class TestBank(unittest.TestCase):
    """
    """

    def setUp(self):
        super(TestBank, self).setUp()
        self.logger = FileLogging()
        self._first_name = "Python"
        self._last_name = "Tester"
        self._email = "pythontest@python.com"
        self._password = "123123"
        self._username = "PythonMan"
        self._token = ""
        self._userid = 16
        self._http_helpers = HttpCommandHelpers()
        self.logger.info("*************Test Case method starts********")

        self.logger.info(self._testMethodName)  # Shows MethodName of current running method
        self.logger.info("*************Test Case method ends********")

    def tearDown(self):
        super(TestBank, self).tearDown()
        self.logger.info("********TestClass.tearDown starts*************")
        exctype, value, tb = sys.exc_info()[:3]
        if exctype:
            msg = traceback.format_exception(exctype, value, tb)
            self.logger.error(msg)

        self.logger.info("********TestClass.tearDown ends*************\n\n")

    def _login_or_register_user(self):
        """"""
        url = "/backend/users/register"
        user_data = {
            "username": self._username,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "email": self._email,
            "password": self._password

        }
        response = self._http_helpers.send_http_command_post(url, user_data, [httplib.CONFLICT, httplib.OK])
        if response == httplib.CONFLICT:
            self._login()
        else:
            self._token = response["token"]
            self._userid = response["userid"]
            self.logger.info("Response from server:\n%s" % response)

    def _login(self):
        """
        """
        url = "/backend/users/authenticate"
        login_data = {
            "username": self._username,
            "password": self._password
        }
        response = self._http_helpers.send_http_command_post(url, login_data)

        self._token = response["token"]

    def get_list(self):
        """"""

        self._login()
        data = {
            "token": self._token
        }
        url = "/backend/users/%s/lists" % self._userid

        res = self._http_helpers.send_http_command_get(url, data)

        self.logger.info(res)

    def check_token_required(self):
        """"""
        self._login()
        url = "/backend/users/%s/lists" % self._userid
        code_expected = "401"

        res = self._http_helpers.send_http_command_get(url, None, [httplib.UNAUTHORIZED])
        print(res)
        self.assertEqual(str(res['code']), code_expected, "Request accepted without a token.")

    def add_recipe_to_list(self):
        """"""
        url = "/backend/lists/recipe"
        list_id = 20
        recipe_id = 108
        self._login()
        print(self._token)
        data = {
            "token": self._token,
            "user_id": self._userid,
            "list_id": list_id,
            "recipe_id": recipe_id
        }

        res = self._http_helpers.send_http_command_post(url, data, [httplib.CREATED, httplib.OK])
        self.logger.info("Result from server after adding recipe to list: %s" % res)

        url_get = "/backend/users/%s/lists" % self._userid
        data_get = {
            "token": self._token
        }

        res_lists = self._http_helpers.send_http_command_get(url_get, data_get)
        self.logger.info("Result from fetching lists:\n%s" % res_lists)

        for list in res_lists["lists"]:
            if list["list_id"] == str(list_id):
                if str(recipe_id) not in list["recipes"]:
                    print(list["recipes"])
                    raise AssertionError("The recipe was NOT added to the list.")

    def create_user(self):
        """
        """
        url_register = "/backend/users/register"
        url_authenticate = "/backend/users/authenticate"
        username = "RandomUser"
        first_name = "Bourgh"
        last_name = "Smith"
        password = "123123"

        data_register = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password
        }

        res = self._http_helpers.send_http_command_post(url_register, data_register, [httplib.CREATED, httplib.OK, httplib.ACCEPTED])
        self.logger.info("Result from registering a user: %s" % res)

        time.sleep(5)

        data_auth = {
            "username": username,
            "password": password
        }

        res_auth = self._http_helpers.send_http_command_post(url_authenticate, data_auth, [httplib.OK])
        if not res_auth["token"]:
            raise AssertionError("No token as sent back for the new user!\n"
                                 "Result from the server:\n %s" % res_auth)

    def suite(self):
        """"""
        suite = unittest.TestSuite()
        suite.addTest(TestBank('get_list'))
        suite.addTest(TestBank('check_token_required'))
        suite.addTest(TestBank('add_recipe_to_list'))
        # suite.addTest(TestBank('create_user'))
        return suite
