from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('news/', views.news, name='news'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.pageN, name='about'),
    path('memberships/', views.memberships_list, name='memberships'),
    path('order/create/<int:membership_id>/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('membership/<int:membership_id>/reviews/', views.membership_reviews, name='membership_reviews'),
    path('membership/<int:membership_id>/add-review/', views.add_review, name='add_review'),
]