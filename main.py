import http.client as httplib
import json
import unittest
from TestClass import TestBank

if __name__ == "__main__":
    # print("hej")
    # c = httplib.HTTPSConnection("recipe.bhsi.xyz")
    # c.request("GET", "/backend/ratings")
    # response = c.getresponse()
    # print (response.status, response.reason)
    # data = response.read()
    # print (data)
    #
    # c.close()
    # print("hdsja")
    tst = TestBank()
    suite = tst.suite()

    runner = unittest.TextTestRunner()
    runner.run(suite)
