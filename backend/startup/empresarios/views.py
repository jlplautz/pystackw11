from datetime import date

from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from .models import Documento, Empresas, Metricas


def cadastrar_empresa(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/login')

    if request.method == 'GET':
        return render(request, 'empresarios/cadastrar_empresas.html')


def listar_empresas(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/login')

    # TODO: REalizar os filtros das empresas
    if request.method == 'GET':
        empresas = Empresas.objects.filter(user=request.user)
        return render(
            request, 'empresarios/listar_empresas.html', {'empresas': empresas}
        )


@property
def status(self):
    if date.today() > self.data_final_captacao:
        return mark_safe(
            '<span class="badge bg-success">Captação finalizada</span>'
        )
    return mark_safe('<span class="badge bg-primary">Em captação</span>')


def empresa(request, id):
    empresa = Empresas.objects.get(id=id)

    if empresa.user != request.user:
        messages.add_message(
            request, constants.ERROR, 'Desculpe, esta empresa não é a sua.'
        )
        return redirect(f'/empresarios/lista_empresas')

    if request.method == 'GET':
        documentos = Documento.objects.filter(empresa=empresa)
        return render(
            request,
            'empresarios/empresa.html',
            {
                'empresa': empresa,
                'documentos': documentos,
            },
        )


def add_doc(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    arquivo = request.FILES.get('arquivo')
    extensao = arquivo.name.split('.')

    if empresa.user != request.user:
        messages.add_message(
            request, constants.ERROR, 'Desculpe, esta empresa não é a sua.'
        )
        return redirect(f'/empresarios/lista_empresas')

    if extensao[1] != 'pdf':
        messages.add_message(request, constants.ERROR, "Envie apenas PDF's")
        return redirect(f'/empresarios/empresa/{empresa.id}')

    if not arquivo:
        messages.add_message(request, constants.ERROR, 'Envie um arquivo')
        return redirect(f'/empresarios/empresa/{empresa.id}')

    documento = Documento(empresa=empresa, titulo=titulo, arquivo=arquivo)

    documento.save()

    messages.add_message(
        request, constants.SUCCESS, 'Arquivo cadastrado com sucesso'
    )

    return redirect(f'/empresarios/empresa/{empresa.id}')


def excluir_dc(request, id):
    documento = Documento.objects.get(id=id)

    if documento.empresa.user != request.user:
        messages.add_message(
            request, constants.ERROR, 'Esse documento não é seu'
        )
        return redirect(f'/empresarios/empresa/{empresa.id}')

    documento.delete()
    messages.add_message(
        request, constants.SUCCESS, 'Documento excluído com sucesso'
    )
    return redirect(f'/empresarios/empresa/{documento.id}')


def add_metrica(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    valor = request.POST.get('valor')

    metrica = Metricas(empresa=empresa, titulo=titulo, valor=valor)
    metrica.save()

    messages.add_message(
        request, constants.SUCCESS, 'Métrica cadastrada com sucesso'
    )
    return redirect(f'/empresarios/empresa/{empresa.id}')
