from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.Home, name="home"),

    path('e/', views.Earning, name="earning"),

    path('a/', views.Amount, name="amount"),

    path('n/', views.Note, name="note"),

    path('c/', views.Calender, name="calendar"),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
]