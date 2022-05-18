import http.client as httplib
import time
import json
import types
import socket


class HttpCommandHelpers:
    """
    """

    class Method:
        """enum of methods"""
        GET = "GET"
        PUT = "PUT"
        POST = "POST"
        DELETE = "DELETE"

    def __init__(self):
        """"""
        self._base_url = "recipe.bhsi.xyz"
        #c.request("GET", "/backend/ratings")

    def _send_http_command(self, method, url, data, response_expected):
        """
        :param method:
        :param url:
        :param data:
        :param response_expected:
        :return:
        """
        headers = {
            'content-type': "application/json",
        }

        conn = None
        try:
            conn = httplib.HTTPSConnection("recipe.bhsi.xyz")
        except Exception as e:
            print("The HTTPS connection to the server went wrong:\n%s" % e)

        if data:
           data = json.dumps(data)

        conn.request(method, url, data, headers)

        response = conn.getresponse()
        if response.status == httplib.CONFLICT:
            return response.status

        if response.status not in response_expected:
            msg = "Incorrect response from the server: got: %s\n, expected: %s\n, reason: %s\n" % \
                  (response.status, response_expected, response.reason)
            conn.close()
            if response.status in [httplib.NOT_FOUND, httplib.METHOD_NOT_ALLOWED]:
                pass
                msg += "\nThe server does NOT allow this request"
                print("The server does not allow this request.")
                return msg
            return msg

        data = response.read()
        if len(data.strip()) != 0:
            print(data)
            out = json.loads(data)
            conn.close()

            return out

        conn.close()

    def send_http_command_get(self, url, data=None, resp_expected=None):
        """"""
        if resp_expected is None:
            resp_expected = [httplib.OK]
        return self._send_http_command(self.Method.GET, url, data, resp_expected)

    def send_http_command_put(self, url, data, resp_expected=None):
        """"""
        if resp_expected is None:
            resp_expected = [httplib.OK]
        return self._send_http_command(self.Method.PUT, url, data, resp_expected)

    def send_http_command_post(self, url, data, resp_expected=None):
        """"""
        if resp_expected is None:
            resp_expected = [httplib.OK]
        return self._send_http_command(self.Method.POST, url, data, resp_expected)
