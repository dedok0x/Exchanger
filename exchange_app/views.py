from django.shortcuts import render
import requests


def exhange(request):
    response = requests.get(url='https://api.exchangerate-api.com/v4/latest/USD').json()
    currencies = response.get('rates')

    if request.method == 'GET':
        context = {
            'currencies': currencies
        }

        return render(request=request, template_name='exchange_app/index.html', context=context)

    if request.method == "POST":
        try:
            from_amount = float(request.POST.get('from-amount'))
            from_curr = request.POST.get('from-curr')
            to_curr = request.POST.get('to-curr')
            converted_amount = round(currencies[to_curr] / currencies[from_curr] * from_amount, 2)

            context = {
                "currencies": currencies,
                'converted_amount': converted_amount,
                'from_amount': from_amount,
                "from_curr": from_curr,
                "to_curr": to_curr
            }

            return render(request=request, template_name='exchange_app/index.html', context=context)
        except ValueError:
            context = {
                "currencies": currencies,
                'error': True
            }
            return render(request=request, template_name='exchange_app/index.html', context=context)