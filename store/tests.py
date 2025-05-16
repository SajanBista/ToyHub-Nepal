from django.test import TestCase
from django.urls import reverse
from store.models import Product  # assuming you have this model

class ProductModelTest(TestCase):

    def setUp(self):
        # Create a sample product to test with
        self.product = Product.objects.create(
            name='Test Toy',
            price=9.99,
            age_group='3-5',
            category='Educational'
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Toy')
        self.assertEqual(float(self.product.price), 9.99)

class HomePageViewTest(TestCase):

    def test_homepage_status_code(self):
        url = reverse('home')  # use the name of your home urlpattern
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_homepage_template_used(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'home.html')
