import datetime
import requests
from .models import Category, Article 

def weather(request):
    city = 'fergana'
    token = '2c815f1b25a0444b813174832260105'

    try:
        response = requests.get(f'https://api.weatherapi.com/v1/current.json?q={city}&key={token}', timeout=5)
        data = response.json()

        temp_c = data.get('current').get('temp_c')
        icon = data.get('current').get('condition').get('icon')
    except Exception:
        temp_c = "--"
        icon = None

    return {
        'temp_c': temp_c,
        'icon': icon,
        'time': datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
    }

def nav_categories(request):
    categories = Category.objects.all()
    return {
        'nav_categories': categories,
    }

def carousel(request):

    articles = Article.objects.order_by('-created_at')[:10]
    return {
        'carousel_articles': articles,
    }