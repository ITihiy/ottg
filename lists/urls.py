from django.urls import path

from lists import views


app_name = 'lists'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('lists/<int:list_id>/', views.view_list, name='view_list'),
    path('lists/new', views.new_list, name='new_list'),
    path('lists/users/<str:owner>/', views.my_lists, name='my_lists')
]
