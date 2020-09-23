from django.urls import path
from . import views
urlpatterns = [
    path('product/<str:action>/', views.product_action),
    path('supplier/<str:action>/', views.supplier_action)
]