def soma(a, b):
    return a + b

def div(a, b):
    if b == 0:
        raise ZeroDivisionError("Divisão por zero")
    return a / b
