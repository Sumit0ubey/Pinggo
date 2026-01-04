from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect('chat_base')
    return render(request, 'home.html')
