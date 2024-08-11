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


def cadastrar_empresa(request):
    if request.method == 'GET':
        return render(
            request,
            'empresarios/cadastrar_empresa.html',
            {
                'tempo_existencia': Empresas.tempo_existencia_choices,
                'areas': Empresas.area_choices,
            },
        )
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        tempo_existencia = request.POST.get('tempo_existencia')
        descricao = request.POST.get('descricao')
        data_final = request.POST.get('data_final')
        percentual_equity = request.POST.get('percentual_equity')
        estagio = request.POST.get('estagio')
        area = request.POST.get('area')
        publico_alvo = request.POST.get('publico_alvo')
        valor = request.POST.get('valor')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')

        # Todo: Realizar validação de campos
        try:
            empresa = Empresas(
                user=request.user,
                nome=nome,
                cnpj=cnpj,
                site=site,
                tempo_existencia=tempo_existencia,
                descricao=descricao,
                data_final_captacao=data_final,
                percentual_equity=percentual_equity,
                estagio=estagio,
                area=area,
                publico_alvo=publico_alvo,
                valor=valor,
                pitch=pitch,
                logo=logo,
            )
            empresa.save()
        except:
            messages.add_message(
                request, constants.ERROR, 'Erro interno do sistema'
            )
            return redirect('/empresarios/cadastrar_empresa')

        messages.add_message(
            request, constants.SUCCESS, 'Empresa criada com sucesso'
        )
        return redirect('/empresarios/cadastrar_empresa')


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
