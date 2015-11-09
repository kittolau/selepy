from random import randint
import math

class AbstractNameGenerator(object):

    def __init__(self):
        return

    def nameGen(self,firstNames, lastNames):
        names2 = firstNames
        names1 = lastNames

        firstNameRnd = int( math.floor( randint(0,len(names2) - 1) ) )
        lastNameRnd = int( math.floor( randint(0,len(names1) - 1) ) )

        first_name = firstNames[firstNameRnd].lower()
        last_name = lastNames[lastNameRnd].lower()
        return {'first_name': first_name, 'last_name': last_name}

