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
    return ','.join(re)


def displayCart(carts):
    length = len(carts)
    total = 0
    totalProduct = 0
    for i in range(length):
        totalProduct = carts[i]['amount'] * carts[i]['price_sale']
        total += totalProduct
        carts[i]['total'] = convertCurrency(totalProduct)
        carts[i]['price_sale'] = convertCurrency(carts[i]['price_sale'])
    return carts, total