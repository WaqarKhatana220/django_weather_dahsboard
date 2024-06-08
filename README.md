# Project Setup
## Django Project Setup
Clone the repository and `cd` into the `weather_project` directory. Install the necessary packages listed in the `requirements.txt` file using the following command:
```
pip install -r requirements.txt
```

## Database Setup
Make sure you have PostgreSQL setup on your machine. The database configuration settings are given in the `settings.py` file, and are listed here for convenience. Use this configuration to setup a database on your machine or change the cofiguration to match your database settings:
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'weather_db',
        'USER': 'weather_user',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}
```

## OpenWeatherMap API
Visit https://openweathermap.org/ and generate an API key. Copy and paste this API key in `weather_project/weather/views.py` file at this location:
```py
async def get_weather_data(city):
    api_key = '' # Paste your API key here
    ...
```

# Running
Once the project has been setup and database up and running, navigate to the `weather_project` directory and execute the following commands one-by-one:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Go to http://localhost:8000/api/auth/register/ using your browser and register using valid credentials.
> Note: The password must be atleast 8 characters long and must contain atleast 1 uppercase, 1 lowercase, and 1 special characters.

# App Workflow
Register -> Login -> Weather Dashboard (Main Page) <br>
In the Weather Dashboard, enter a city name in the 'Search Weather' search bar to get weather details of the queried city. You can also see your 5 recent most searches upon clicking on the search bar. You can also add favorite cities using the "Add Favorite City" feature. Click on any of your favorite cities to quickly access the weather data for it.
![Weather Dashboard](https://github.com/WaqarKhatana220/django_weather_dahsboard/blob/main/Readme%20Assets/Screenshot%202024-06-08%20223807.png)

# Technologies
The main technology used to develope this project is Python and its libraries: <br>
**Backend:** Django <br>
**Frontend:** Django Templating Engine <br>
**Database:** Postgres (with Django ORM) <br><br>
Other frameworks/libraries used are:
- djangorestframework
- djangorestframework-simplejwt
- httpx (for async calls)
- psycopg2-binary
- requests

The project follows the MTV architecture of Django. The project contains 2 apps that allow separation of concern;
- `users` for user management and authentication
- `weather` for Weather Dashboard functionality
