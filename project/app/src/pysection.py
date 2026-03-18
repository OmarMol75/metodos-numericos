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

        result_str = ""

        roots_founded = set()

        for pair in pairs:

            a_ = pair[0]
            b_ = pair[1]

            if a_ == b_:
                roots_founded.add(round(a_, 4))
                continue

            iteration = 0
            fa = func(a_)
            while ((b_) - (a_)) > tolerance and iteration < max_iterations:
                print(f'{a_}, {b_}')
                c = ((a_) + (b_))/2
                fc = func(c)

                if fc == 0:
                    a_= b_ = c
                    break

                if fc * fa < 0:
                    b_ = c
                else:
                    a_ = c
                    fa = fc

                
                iteration += 1
            roots_founded.add(round((a_ + b_)/2, 4))

        if not roots_founded:
            result_str = "No existen raices para esta ecuación"
        else:
            for r in sorted(roots_founded):

                result_str += f'Raíz en: {r:.4f}<br/>'
    
        request.session['result_str'] = result_str
        request.session['function'] = givenFunction
    return redirect('index')

def findIntervals(givenFunction):
    func = f(givenFunction)
    i = -5
    step = 0.5
    pairs = []
    while i < 5:
        fi = func(i)
        fj = func(i+step)
        if (fi*fj) < 0:
            pairs.append([i, i+step]) 
        elif fi == 0:   
            pairs.append([i,i])   
        i += step
    return pairs