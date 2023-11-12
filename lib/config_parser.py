import json

class ConfigParser(object):
  _instance = None
  config = {}
  def __new__(cls):
    if not isinstance(cls._instance, cls):
      cls._instance = object.__new__(cls)
    return cls._instance

  def get_config(self): 
    if (self.config != {}):
      print("loaing config from memory...")
      return self.config

    print("loading config from file...")

    f_io = open("./config.json")
    self.config = json.load(f_io)
    f_io.close()

    return self.config


