import yaml
import os
import os.path


DS = '/'

WEBOT_ENV = os.environ.get('WEBOT_ENV', 'development')
APP_CONFIG_FILENAME = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.yml')

class ConfigFileError(Exception):
    def __init__(self,*args,**kwargs):
        # Call the base class constructor with the parameters it needs
        super(ConfigFileError, self).__init__(*args,**kwargs)


class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    if isinstance(v, dict):
                        self[k] = Map(v)
                    else:
                        self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                if isinstance(v, dict):
                    self[k] = Map(v)
                else:
                    self[k] = v

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise ConfigFileError("Config file missing key {attr}".format(attr=attr))

    # def __setattr__(self, key, value):
        # self.__setitem__(key, value)

    # def __setitem__(self, key, value):
        # super(Map, self).__setitem__(key, value)
        # self.__dict__.update({key: value})

    # def __delattr__(self, item):
        # self.__delitem__(item)

    # def __delitem__(self, key):
        # super(Map, self).__delitem__(key)
        # del self.__dict__[key]

with open(APP_CONFIG_FILENAME, 'r') as ymlfile:
    #load type of config base on WEBOT_ENV
    configHash = yaml.load(ymlfile)[WEBOT_ENV]

    #setup default value
    if "root" not in configHash:
        configHash["root"] = os.path.abspath(os.path.join(__file__,os.pardir,os.pardir))

    appConfig = Map(configHash)

