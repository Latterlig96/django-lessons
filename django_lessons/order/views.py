from typing import Any, Dict

import stripe
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, View

from .models import Order, Product

stripe.api_key = settings.STRIPE_PUBLISHABLE_KEY

class ProductLandingView(TemplateView):
    template_name = "order/landing.html"

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        product = Product.objects.get(id=self.kwargs["pk"])
        context = super().get_context_data(**kwargs)
        context.update({
            'product': product,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY
        })
        return context

class SucessView(TemplateView):
    template_name = "order/sucess.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        product = Product.objects.get(id=self.kwargs['pk'])
        order = Order.objects.create(student=self.request.user,
                                     product=product)
        user = self.request.user
        user.is_subscriber = True
        user.save()
        return super().dispatch(request, *args, **kwargs)

class CancelView(TemplateView):
    template_name = "order/cancel.html"

class StripeCheckoutSessionView(View):

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        product = Product.objects.get(id=self.kwargs["pk"])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=self.request.user.email,
            line_items = [
                {
                    'price_data': {
                        'currency': product.currency,
                        'unit_amount_decimal': product.price,
                        'product': product.stripe_id
                    },
                    'quantity': 1
                }
            ],
            mode='payment',
            success_url=reverse('order:success', kwargs={'pk': product.id}),
            cancel_url=reverse('order:cancel')
        )
        return JsonResponse(data = {
            'id': checkout_session.id
        })
