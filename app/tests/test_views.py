from django.test import TestCase
from django.urls import reverse

class CategoryListTestCase(TestCase):
    def test_view_url_exist_location(self):
        response = self.client.get('/products/categories/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_reversed_by_name(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)

    def test_view_set_categories_in_context(self):
        response = self.client.get(reverse('categories'))
        # self.assertTrue('categories' in response.context)
        self.assertIn('categories2', response.context)

    def test_view_correct_template(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/categories.html')

