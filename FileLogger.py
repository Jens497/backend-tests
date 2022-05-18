import logging
from time import gmtime, strftime

class FileLogging(object):
  """
  Handles all the logging that comes from the tests
  """
  def __init__(self):
    string_f = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    d = string_f.replace(":", "-")
    fileWrite = "log_res_%s" % d
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=fileWrite, level=logging.INFO, format=FORMAT)

  def debug(self, msg):
    logging.debug(msg)

  def info(self, msg):
    logging.info(msg)

  def warn(self, msg):
    logging.warning(msg)

  def error(self, msg):
    logging.error(msg)
