from django.urls import path, include


app_name = 'core'

urlpatterns = [
	path('api/', include('places.api.endpoints', namespace='api')),
]