import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from .models import Price
from django.views.generic import TemplateView
from .models import Product
from django.shortcuts import redirect
stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="T-Shirt")
        prices = Price.objects.filter(product=product)
        context = super(ProductLandingPageView,
                        self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        domain = "https://yourdomain.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price.stripe_price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=domain + '/success/',
                cancel_url=domain + '/cancel/',
            )
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
