from django.shortcuts import render

def show_main(request):
    context = {
        'npm': '2306217071',
        'name': 'Dave',
        'class': 'PBP E'
    }

    return render(request, 'main.html', context)
