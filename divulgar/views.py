from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tag, Raca, Pet
from django.contrib import messages
from django.contrib.messages import constants
from adotar.models import PedidoAdocao
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@login_required
def novo_pet(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        racas = Raca.objects.all()

        context = {
            'tags': tags,
            'racas': racas
        }

        return render(request, 'novo_pet.html', context)

    elif request.method == 'POST':
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        tags = request.POST.getlist('tags')
        raca = request.POST.get('raca')

        # falta fazer as validações

        # PASSO 1: Criar a instância pet e salvar as propriedades
        # da classe Pet, exceto a propriedade tag, que é um ManyToManyField.
        pet = Pet(
            usuario=request.user, # request.user é o usuário local
            foto=foto,
            nome=nome,
            descricao=descricao,
            estado=estado,
            cidade=cidade,
            telefone=telefone,
            raca_id=raca # raca_id é para pegar o nome da raça pelo id
        )

        pet.save()

        # PASSO 2: Salavar as tags no banco. Usaremos o for para percorrer
        # a classe Tag e pegar pelo id, e salvar com pet.save().
        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            pet.tags.add(tag)
            pet.save()
            tags = Tag.objects.all()
            racas = Raca.objects.all()
            messages.add_message(request, constants.SUCCESS, 'Novo pet cadastrado com sucesso!')
            return redirect('/divulgar/seus_pets')

            context = {
                'tags': tags,
                'racas': racas
            }

            return render(request, 'novo_pet.html', context)


@login_required
def seus_pets(request):
   if request.method == 'GET':
       pets = Pet.objects.filter(usuario=request.user)


       context = {
           'pets': pets
       }
       return render(request, 'seus_pets.html', context)


@login_required
def remover_pet(request, id):
    pet = Pet.objects.get(id=id)

    if not pet.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Esse pet não é seu!')
        return redirect('/divulgar/seus_pets')

    pet.delete()

    messages.add_message(request, constants.SUCCESS('Pet removido com sucesso!'))
    return redirect('/divulgar/seus_pets')

@login_required
def ver_pet(request, id):
    if request.method == 'GET':
        pet = Pet.objects.get(id=id)
        return render(request, 'ver_pet.html', {'pet': pet})

@login_required
def ver_pedido_adocao(request):
    if request.method == "GET":
        pedidos = PedidoAdocao.objects.filter(usuario=request.user).filter(status="AG")
        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos})

@login_required
def dashboard(request):
    if request.method == 'GET':
        return render(request, 'dashboard.html')

@csrf_exempt
def api_adocoes_por_raca(request):
    racas = Raca.objects.all()

    qtd_adocoes = []

    for raca in racas:
        #Solicitação para pedido de adoção por status aprovado.
        adocoes = PedidoAdocao.objects.filter(pet__raca=raca).filter(status='AP').count()

        # Solicitação para pedido de adoção por status solicitação.
        #adocoes = PedidoAdocao.objects.filter(pet__raca=raca).count()
        qtd_adocoes.append(adocoes)

    racas = [raca.raca for raca in racas]
    data = {'qtd_adocoes': qtd_adocoes,
            'labels': racas
            }

    return JsonResponse(data)

