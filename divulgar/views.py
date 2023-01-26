from django.shortcuts import render

# Create your views here.
def novo_pet(request):
    return render(request, 'novo_pet.html')
