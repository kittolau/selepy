from service import *

db = PymongoManger().getNew()
distinct_domain = db.users.find().distinct("web_accounts.domain");

for domain in distinct_domain:
    account_count = db.users.find({"web_accounts.domain":domain}).count()
    print "%s: %d" % (domain,account_count)
