from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('auth/', include('users.urls')),
    path('store/', include('store.urls')),
    path('payments/', include('payments.urls')),
]