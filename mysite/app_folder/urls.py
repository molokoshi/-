"""URL for app"""
from django.urls import path
from . import views

app_name = 'app_folder'
urlpatterns = [
    path('top_page/', views.HomeView.as_view(), name='top_page'),
    path('search_id/', views.SearchView.as_view(), name='search_id'),
    path('list/', views.ListViews.as_view(), name='list'),
    path('detail/<int:base_id>/', views.DetailViews.as_view(), name='detail'),
# path('detail_date/<int:base_id>/', views.DetailViews_date.as_view(), name='detail_date'),
]
