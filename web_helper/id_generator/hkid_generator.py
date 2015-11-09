from random import randint

class HKIDGenerator():
    IDCharMapping = {
    0 : '0',
    1 : '1',
    2 : '2',
    3 : '3',
    4 : '4',
    5 : '5',
    6 : '6',
    7 : '7',
    8 : '8',
    9 : '9',
    10:'A',
    11:'B',
    12:'C',
    13:'D',
    14:'E',
    15:'F',
    16:'G',
    17:'H' ,
    18:'I' ,
    19:'J' ,
    20:'K' ,
    21:'L',
    22:'M',
    23:'N' ,
    24:'O' ,
    25:'P' ,
    26:'Q' ,
    27:'R',
    28:'S',
    29:'T' ,
    30:'U' ,
    31:'V' ,
    32:'W' ,
    33:'X',
    34:'Y',
    35:'Z'}

    def getHKID(self):

        resultID = []
        resultIDNumber = []

        #first char
        firstNumber= randint(10,35)
        resultID.append(self.IDCharMapping[firstNumber])
        resultIDNumber.append(firstNumber)

        #mid number
        for r in range(0, 6):
            number = randint(0,9)
            resultID.append(str(number))
            resultIDNumber.append(number)

        #find last checksum number
        resultID.append(self.IDCharMapping[11 - self.__getHKIDCheckSum(resultIDNumber)])

        return "".join(resultID)

    def __getHKIDCheckSum(self,resultIDNumber):
        sum = 58*9 + resultIDNumber[0]*8 + resultIDNumber[1]*7 + resultIDNumber[2]*6 + resultIDNumber[3]*5 + resultIDNumber[4]*4 + resultIDNumber[5]*3 + resultIDNumber[6]*2

        checkSum = sum % 11
        return checkSum

