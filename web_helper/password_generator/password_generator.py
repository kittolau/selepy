from random import randint
import math

class PasswordGenerator():

    def __init__(self,length):
        self.password_seed                   = ""
        self.password_constraints            = []
        self.reserved_constraints_char_count = 0
        self.required_password_length        = length

    def __addSeedCharList(self,char_list,at_least_have_count):
        if at_least_have_count is not None and not isinstance( at_least_have_count, int ):
            raise Exception("at_least_have_count expect None or int")

        self.password_seed += char_list

        if at_least_have_count is not None:
            self.reserved_constraints_char_count += at_least_have_count

            if self.reserved_constraints_char_count > self.required_password_length:
                raise Exception("at_least_have_count should not bigger than required_password_length")

            self.password_constraints.append({
                "char_list":char_list,
                "at_least_have_count":at_least_have_count
                })

    def resetInculde(self,length):
        self.password_seed                   = ""
        self.password_constraints            = []
        self.reserved_constraints_char_count = 0
        self.required_password_length        = length

    def AsSecurePasswordSetting(self):
        self.resetInculde(8)
        self.includeLowerCase(2).includeUpperCase(2).includeNumber(2)
        return self

    def includeLowerCase(self,at_least_have_count=None):
        self.__addSeedCharList("abcdefghijklmnopqrstuvwxyz",at_least_have_count)
        return self

    def includeUpperCase(self,at_least_have_count=None):
        self.__addSeedCharList("ABCDEFGHIJKLMNOPQRSTUVWXYZ",at_least_have_count)
        return self

    def includeNumber(self,at_least_have_count=None):
        self.__addSeedCharList("0123456789",at_least_have_count)
        return self

    def includeSymbol(self,at_least_have_count=None):
        self.__addSeedCharList("!#$%&*+-=?@^_|",at_least_have_count)
        return self

    def includeChar(self,charList,at_least_have_count=None):
        self.__addSeedCharList(charList,at_least_have_count)
        return self

    def buildRawPassword(self,length):
        res_password=""
        seed_length = len(self.password_seed)

        if seed_length is 0:
            raise Exception("password_seed must have something at least")

        for i in range(0, length):
            rand = int( math.floor( randint(0,seed_length - 1) ) )
            res_password += self.password_seed[rand:rand+1]
        return res_password

    def generate(self):
        res_password= self.buildRawPassword(self.required_password_length - self.reserved_constraints_char_count)

        for constraint in self.password_constraints:
            char_list           = constraint["char_list"]
            at_least_have_count = constraint["at_least_have_count"]

            required_password_length    = self.required_password_length
            constraint_char_list_length = len(char_list)

            for i in range(0,at_least_have_count):
                char_list_random_index = int( math.floor( randint(0,constraint_char_list_length - 1) ) )
                random_char            = char_list[char_list_random_index:char_list_random_index+1]

                rand_position_to_add = int( math.floor( randint(0,constraint_char_list_length - 1) ) )
                res_password         = res_password[rand_position_to_add:] + random_char + res_password[:rand_position_to_add]

        return res_password
