from accounts.models import StudentUser
from django.db.utils import IntegrityError
from django.test import TestCase
from order.models import Order, Product


class TestProduct(TestCase):
    def setUp(self):
        self.correct_case = {
            "name": "TestProduct",
            "price": 20.0,
            "currency": "PLN",
            "stripe_product_id": "TestProduct",
        }

    def test_product_model(self):
        Product.objects.create(**self.correct_case)
        self.assertTrue(Product.objects.filter(name="TestProduct").exists())

    def test_fail_case_product_model_without_name(self):
        self.correct_case.update({"name": None})
        with self.assertRaises(IntegrityError) as context:
            Product.objects.create(**self.correct_case)
            self.assertFalse(
                Product.objects.filter(stripe_product_id="TestProduct").exists()
            )

    def test_fail_case_product_model_negative_price(self):
        self.correct_case.update({"price": -30.0})
        with self.assertRaises(IntegrityError) as context:
            Product.objects.create(**self.correct_case)
            self.assertFalse(
                Product.objects.filter(stripe_product_id="TestProduct").exists()
            )

    def test_fail_case_product_model_unsupported_currency(self):
        self.correct_case.update({"currency": "Unknown"})
        with self.assertRaises(IntegrityError) as context:
            Product.objects.create(**self.correct_case)
            self.assertFalse(
                Product.objects.filter(stripe_product_id="TestProduct").exists()
            )

    def test_fail_case_product_model_without_currency(self):
        self.correct_case.update({"currency": None})
        with self.assertRaises(IntegrityError) as context:
            Product.objects.create(**self.correct_case)
            self.assertFalse(
                Product.objects.filter(stripe_product_id="TestProduct").exists()
            )

    def test_fail_case_product_model_without_stripe_product_id(self):
        self.correct_case.update({"stripe_product_id": None})
        with self.assertRaises(IntegrityError) as context:
            Product.objects.create(**self.correct_case)
            self.assertFalse(
                Product.objects.filter(stripe_product_id="TestProduct").exists()
            )

    def test_product_model_display_price_method(self):
        Product.objects.create(**self.correct_case)
        product = Product.objects.get(name="TestProduct")
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_display_price(), 2000.0)


class TestOrder(TestCase):
    def setUp(self):
        StudentUser.objects.create(
            username="TestUser",
            first_name="TestFirstName",
            last_name="TestLastName",
            email="teststudent@gmail.com",
            password="testPassword",
        )
        Product.objects.create(
            name="TestProduct",
            price=20.0,
            currency="PLN",
            stripe_product_id="TestProduct",
        )
        self.correct_case = {
            "student": StudentUser.objects.get(username="TestUser"),
            "product": Product.objects.get(name="TestProduct"),
        }

    def test_order_model(self):
        Order.objects.create(**self.correct_case)
        self.assertTrue(Order.objects.filter(student__username="TestUser"))

    def test_fail_case_test_order_without_student(self):
        self.correct_case.update({"student": None})
        with self.assertRaises(IntegrityError) as context:
            Order.objects.create(**self.correct_case)
            self.assertEqual(Order.objects.all(), 0)

    def test_fail_case_test_order_without_product(self):
        self.correct_case.update({"product": None})
        with self.assertRaises(IntegrityError) as context:
            Order.objects.create(**self.correct_case)
            self.assertFalse(Order.objects.filter(student__username="TestUser"))
