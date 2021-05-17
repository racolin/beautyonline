from django.test import TestCase
# Create your tests here.

def convertCurrency(value: int):
    v = str(value)
    length = len(v)
    re = []
    temp = ''
    for i in v:
        temp += i
        length -= 1
        if length % 3 == 0:
            re.append(temp)
            temp = ''
    return ', '.join(re)
