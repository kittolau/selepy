
from service import PymongoManger
from service.logger_manager import logger
from web_helper.name_generator import ChineseNameGenerator, JapaneseNameGenerator
from web_helper.password_generator.password_generator import PasswordGenerator
import pymongo
import datetime
from random import randrange,randint,shuffle
import math
from pymongo.errors import DuplicateKeyError

country            = "jp"
name_generator     = JapaneseNameGenerator()
password_generator = PasswordGenerator(8).AsSecurePasswordSetting()
female_count       = 239
male_count         = 761

def generateBirthDay():
    offset_days = randrange(-365,365)
    age_from_now = randrange(16,28)
    birth_day = datetime.datetime.now() - datetime.timedelta(days= 365 * age_from_now + offset_days)
    return birth_day

def generateUsername(last_name,first_name):
    username_elements = []

    should_add_number = True
    if should_add_number:

        upper_length = "99"
        for x in range(0,2):
            upper_length += "9"

        number = str(int( math.floor( randint(1,int(upper_length)))))
        username_elements.append(number)

    randomized_first_name = first_name.replace(" ", "")
    randomized_first_name = randomized_first_name[:int( math.floor( randint(1,len(first_name) - 1) ) )]
    randomized_first_name = randomized_first_name.strip()
    username_elements.append(randomized_first_name)

    randomized_last_name = last_name.replace(" ", "")
    randomized_last_name = randomized_last_name.strip()
    username_elements.append(randomized_last_name)

    shuffle(username_elements)

    username = "".join(username_elements)

    if username[0].isdigit():
        username = randomized_last_name[0] + username

    return username

def generateHKPhone():
    first_number = ["2","3","9"][int( math.floor( randint(0,2)))]
    phone =  str(int(math.floor( randint(1000000,9999999))))
    return str(first_number + phone)

def seedHKUser(usernameDict,sex):
    doc                     = usernameDict
    doc["country"]          = country
    doc["sex"]              = "m"

    birht_day               = generateBirthDay()
    doc["birth_day"]        = birht_day
    doc["birth_day_year"]   = str(birht_day.year)
    doc["birth_day_month"]  = str(birht_day.month)
    doc["birth_day_day"]    = str(birht_day.day)

    doc["default_password"]     = password_generator.generate()
    doc["default_username"] = generateUsername(username["last_name"],username["first_name"])

    doc["phone"]            = generateHKPhone()
    doc["phone_code"]       = "+852"

    doc["seed_at"]          = datetime.datetime.utcnow()

    doc["web_accounts"]      = []

    try:
        users.insert(doc)
    except DuplicateKeyError, e:
        logger.warn("Dulplicate username: %s" % username["default_username"])

users = PymongoManger().getNew().users
users.create_index([("default_username", pymongo.ASCENDING)],unique=True)
# users.create_index([("web_accounts.domain", pymongo.ASCENDING)],unique=True,sparse=True)
for i in range(0,male_count):
    username = name_generator.getMaleName()
    seedHKUser(username,"m")


for i in range(0,female_count):
    username = name_generator.getFemaleName()
    username = name_generator.getMaleName()
    seedHKUser(username,"f")


