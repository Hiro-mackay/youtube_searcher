from django.urls import path
from . import views

app_name = "youtube"

urlpatterns = [
    path('', views.top_search, name="top"),
    path('results/',views.index, name="index"),
    path('<str:video_id>/', views.detaile, name="detail")
]
