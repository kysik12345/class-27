from django.test import TestCase
from app.models import CategoryCreateForm

class CategoryCreateFormtestCase(TestCase):
    def test_field_label(self):
        form = CategoryCreateForm()
        self.assertEqual(form.fields['name'].label, "Категория")