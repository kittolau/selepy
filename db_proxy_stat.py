from service import *

db = PymongoManger(db="proscraper_development").getNew()
distinct_country = db.web_proxys.find().distinct("country");

for country in distinct_country:
    print "\n"
    for proxy_type in ["http","https"]:
        for i in range(1,4):
            proxy_count = db.web_proxys.find({"anonymity_level": i,"country":country,"proxy_type":proxy_type}).count()
            print "%s, %s, anonymity %d : %d" % (country,proxy_type, i, proxy_count)
