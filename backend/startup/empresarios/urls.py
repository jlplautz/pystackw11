from django.urls import path

from . import views

urlpatterns = [
    path(
        'cadastrar_empresas/',
        views.cadastrar_empresa,
        name='cadastrar_empresa',
    ),
]
