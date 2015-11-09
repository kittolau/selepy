from service.logger_manager import logger

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
                    elif isinstance(v, list):
                        for idx, elm in enumerate(v):
                            if isinstance(elm, dict):
                                v[idx] = Map(elm)
                    else:
                        self[k] = v

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise Exception("User missing key {attr}".format(attr=attr))

class User(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    if isinstance(v, dict):
                        self[k] = Map(v)
                    elif isinstance(v, list):
                        for idx, elm in enumerate(v):
                            if isinstance(elm, dict):
                                v[idx] = Map(elm)
                    else:
                        self[k] = v

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise Exception("User missing key {attr}".format(attr=attr))

    def setUsersCollection(self,users_collection):
        self.users_collection = users_collection

    def isWebAccountExist(self,domain):
        accounts = self.web_accounts
        for account in accounts:
            if account.domains == domain:
                return True
        return False

    def getWebAccount(self,domain):
        accounts = self.web_accounts
        for account in accounts:
            if account.domains == domain:
                return account
        return None

    def getBirthDayDayWithLeadingZero(self):
        return "%02d" % self.birth_day_day

    def getBirthDayMonthWithLeadingZero(self):
        return "%02d" % self.birth_day_month

    def generateWebAccountObj(self,domain=None,username=None,password=None):

        if not isinstance(domain, basestring):
            raise Exception("domain expects string in generateWebAccountObj")
        if not isinstance(username, basestring) and username is not None:
            raise Exception("username expects string or None in generateWebAccountObj")
        if not isinstance(password, basestring) and password is not None:
            raise Exception("password expects string or None in generateWebAccountObj")

        if username is None:
            username = self.default_username

        if password is None:
            password = self.default_password

        web_acount = {
            "domain" : domain,
            "username" : username,
            "password" : password
        }

        return web_acount

    def addWebAccount(self,web_acount):
        logger.info("added web account:\nuser: %s\ndomain: %s\nusername: %s\npassword: %s\n" % (
            self.default_username,
            web_acount["domain"],
            web_acount["username"],
            web_acount["password"]
        ))
        self.users_collection.update({"_id":self._id},{"$addToSet":{"web_accounts":web_acount}})

    def getWebAccount(self,domain):
        web_account = next(d for (index, d) in enumerate(self.web_accounts) if d["domain"] == domain)
        if web_account is None:
            raise Exception("username %s does not have web account %s" % self.default_username, domain)
        return web_account



















