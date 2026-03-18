from django.shortcuts import redirect
from sympy import sympify, lambdify, symbols

def f(given):
    x_symbol = symbols('x')
    expression = sympify(given)
    f = lambdify(x_symbol, expression)
    return f


def bisection(request, a, b):
    if request.method =='POST':
        givenFunction = request.POST.get('function')
        func = f(givenFunction)
        fa = func(a)
        tolerance = 0.01

        while ((b) - (a)) > tolerance:
            c = ((a) + (b))/2
            fc = func(c)

            if fc * fa < 0:
                b = c
            elif fc * fa > 0:
                a = c
                fa = fc
        result = (a + b)/2
        request.session['result_str'] = f'{result:6f}'
    return redirect('index')

# For testing only
def pysection(a, b, givenFunction):
    func = f(givenFunction)
    fa = func(a)
    tolerance = 0.01

    while ((b) - (a)) > tolerance:
        c = ((a) + (b))/2
        fc = func(c)

        if fc * fa < 0:
            b = c
        elif fc * fa > 0:
            a = c
            fa = fc

    print((a + b)/2)

if __name__ == "__main__":
    pysection(0, 1, 'x**4 + 3*x**3 -2')