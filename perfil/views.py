from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta, Categoria
from django.contrib.messages import constants
from django.contrib import messages
from extrato.models import Valores
from datetime import datetime
#from django.db.models import Sum

# TODO: Criar função de calcular v3 123
def home(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')
    
    total_entradas = 0
    for entrada in entradas:
        total_entradas += entrada.valor
        
    total_saidas = 0
    for saida in saidas:
        total_saidas = total_saidas + saida.valor
        
    contas = Conta.objects.all()
    
    total_contas = 0
    for conta in contas:
        total_contas+= conta.valor
        
    #TODO: Refatorar códigos repetidos v1 250
        
    return render(request, 'home.html', {'contas': contas, 'total_contas': total_contas, 'total_entradas': total_entradas, 'total_saidas': total_saidas})


def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    #total_contas = contas.aggregate(Sum('valor'))['valor__sum']
    total_contas = 0

    for conta in contas:
        total_contas += conta.valor
    return render(request, 'gerenciar.html', {'contas': contas, 'total_contas': total_contas, 'categorias': categorias})

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')
    
    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')
    
    #TODO: Fazer mais validações
    
    conta = Conta(
        apelido = apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )

    conta.save()

    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!!')
    return redirect('/perfil/gerenciar/')


def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    
    messages.add_message(request, constants.SUCCESS, 'Conta removida com sucesso!!')
    return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))


    #TODO: Fazer validações 

    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso!!')
    return redirect('/perfil/gerenciar/')


def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()

    return redirect('/perfil/gerenciar/')

# TODO: fazer soma com sum v3 116
def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        total = 0
        valores = Valores.objects.filter(categoria=categoria)
        for val in valores:
            total = total + val.valor
        dados[categoria.categoria] = total
    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})


#TODO: fazer calculo financeiro v3 129
def calculo_finaceiro(request):
    ...
