from django.urls import path
from django.contrib.auth import views as auth_views
from store.views.dashboard_views import dashboard
from store.views.item_views import (
    item_list, item_create, item_update, item_delete
)

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', dashboard, name='dashboard'),

    path('items/', item_list, name='item_list'),
    path('items/add/', item_create, name='item_create'),
    path('items/<int:pk>/edit/', item_update, name='item_update'),
    path('items/<int:pk>/delete/', item_delete, name='item_delete'),

]

