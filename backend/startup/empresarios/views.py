from django.shortcuts import render


def cadastrar_empresa(request):
    if request.method == 'GET':
        return render(request, 'cadastrar_empresa.html')
