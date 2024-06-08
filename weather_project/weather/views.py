from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpRequest
from asgiref.sync import sync_to_async
from users.models import FavoriteCity, User
from users.serializers import UserSerializer
import httpx

async def get_weather_data(city):
    api_key = 'd1d4b3d81d5ce0563ddb0c7b55eb41b2'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        return None

class WeatherView(View):
    async def get(self, request: HttpRequest):
        city = request.GET.get('city')
        weather_data = None
        error = None
        favorite_cities = []

        # Wrap session-related operations with sync_to_async
        sync_session = await sync_to_async(request.session.load)()
        recent_searches = sync_session.get('recent_searches', [])

        if city and city not in recent_searches:
            recent_searches.insert(0, city)
            await sync_to_async(self.update_session)(request, recent_searches)
            print('recent_searches:', recent_searches)

        # Use sync_to_async for retrieving the user
        user = await sync_to_async(lambda: request.user if request.user.is_authenticated else None)()

        if user and hasattr(user, 'favorite_cities'):
            favorite_cities = await sync_to_async(list)(user.favorite_cities.all())

        if city:
            weather_data = await get_weather_data(city)
            if weather_data is None:
                error = 'Could not retrieve weather data for the specified city.'

        return render(request, 'weather/weather.html', {'weather_data': weather_data, 'error': error, 'recent_searches': recent_searches, 'favorite_cities': favorite_cities})

    async def post(self, request: HttpRequest):
        print("received")
        city_name = request.POST.get('city2')
        if city_name:
            # Use sync_to_async for retrieving the user
            user = await sync_to_async(lambda: request.user if request.user.is_authenticated else None)()
            if user:
                favorite_city, created = await sync_to_async(FavoriteCity.objects.get_or_create)(city_name=city_name)
                if created:
                    await sync_to_async(user.favorite_cities.add)(favorite_city)
                    await sync_to_async(user.save)()
                    return redirect('get_weather')  # Redirect to the weather page after adding the favorite city

        return render(request, 'weather/weather.html', {'error': 'Invalid request'})

    def update_session(self, request, recent_searches):
        request.session['recent_searches'] = recent_searches
        request.session.modified = True
