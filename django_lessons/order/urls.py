from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('success/', views.SucessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('create-checkout-session/<pk>', views.StripeCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('product/', views.ProductLandingView.as_view(), name='product_landing')
]
