from django.shortcuts import redirect
from sympy import sympify, lambdify, symbols

def f(given):
    x_symbol = symbols('x')
    expression = sympify(given)
    f = lambdify(x_symbol, expression)
    return f


def bisection(request):
    if request.method =='POST':
        if request.session.get('result_str'):
            request.session.pop('result_str')

        givenFunction = request.POST.get('function')
        pairs = findIntervals(givenFunction)

        func = f(givenFunction)

        tolerance = 0.01
        iteration = 0
        max_iterations = 100
        result = 0

        result_str = ""

        for pair in pairs:
            iteration = 0
            result = 0

            a_ = pair[0]
            b_ = pair[1]
            fa = func(a_)
            while ((b_) - (a_)) > tolerance and iteration < max_iterations:
                print(f'{a_}, {b_}')
                c = ((a_) + (b_))/2
                fc = func(c)

                if fc * fa < 0:
                    b_ = c
                elif fc * fa > 0:
                    a_ = c
                    fa = fc
                else:
                    result = c if fc == 0 else a_
                    break
                result = (a_ + b_)/2
                iteration = iteration + 1
            result_str += f'Raíz en: {result:6f}<br/>'
        if(result_str == ""): result_str = "No existen raices para esta ecuación"
        request.session['result_str'] = result_str
        request.session['function'] = givenFunction
    return redirect('index')

def findIntervals(givenFunction):
    func = f(givenFunction)
    i = -100
    step = 0.5
    pairs = []
    while i < 100:
        fi = func(i)
        fj = func(i+step)
        if (fi*fj) <= 0:
            pairs.append([i, i+step])       
        i += step
    return pairs