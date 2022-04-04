from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('success/<pk>/', views.SucessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('create_checkout_session/', views.StripeCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('product/<pk>/', views.ProductLandingView.as_view(), name='product_landing')
]
