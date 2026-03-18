from django.shortcuts import render

def index(request):
    context ={
        'root': request.session.get('result_str')
    }
    return render(request, 'index.html', context)
