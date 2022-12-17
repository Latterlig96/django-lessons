from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse 

from accounts.models import StudentUser
from order.models import Product 
from unittest.mock import MagicMock, patch


class TestProductLandingView(TestCase):
    def setUp(self):
        Product.objects.create(
            name="TestProduct",
            price=20.0,
            currency="USD",
            stripe_product_id="2",            
        )
        StudentUser.objects.create(
            username="TestStudent",
            email="teststudent@gmail.com",
            first_name="testStudentFirstName",
            last_name="testStudentLastName",
            is_student=True,
        )

    def test_product_landing_view(self):
        profile = StudentUser.objects.get(username="TestStudent")
        self.client.force_login(user=profile)
        response = self.client.get(reverse("order:product_landing"))
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "order/landing.html")


class TestSuccessView(TestCase):
    def setUp(self):
        Product.objects.create(
            name="TestProduct",
            price=20.0,
            currency="USD",
            stripe_product_id="2",            
        )
        StudentUser.objects.create(
            username="TestStudent",
            email="teststudent@gmail.com",
            first_name="testStudentFirstName",
            last_name="testStudentLastName",
            is_student=True,
        )

    def test_success_view(self):
        profile = StudentUser.objects.get(username="TestStudent")
        self.client.force_login(user=profile)
        response = self.client.get(reverse("order:success"))
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "order/success.html")


class TestCancelView(TestCase):
    def setUp(self):
        StudentUser.objects.create(
            username="TestStudent",
            email="teststudent@gmail.com",
            first_name="testStudentFirstName",
            last_name="testStudentLastName",
            is_student=True,
        )

    def test_cancel_view(self):
        profile = StudentUser.objects.get(username="TestStudent")
        self.client.force_login(user=profile)
        response = self.client.get(reverse("order:cancel"))
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "order/cancel.html")


class TestStripeCheckoutSessionView(TestCase):
    def setUp(self):
        Product.objects.create(
            name="TestProduct",
            price=20.0,
            currency="USD",
            stripe_product_id="2",            
        )
        StudentUser.objects.create(
            username="TestStudent",
            email="teststudent@gmail.com",
            first_name="testStudentFirstName",
            last_name="testStudentLastName",
            is_student=True,
        )
                        
    @patch("stripe.checkout.Session")
    def test_stripe_post_view(self, stripe_mock):
        class Session:
            @property
            def id(self):
                return 1
        stripe_mock.create = MagicMock(return_value=Session()) 
        profile = StudentUser.objects.get(username="TestStudent")
        self.client.force_login(user=profile)
        response = self.client.post(reverse("order:create-checkout-session", kwargs={"pk": 1}))
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(stripe_mock.create.call_count, 1)
