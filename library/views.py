from django.shortcuts import render

def app_index(request):
    return render(request, 'library/app.html')
