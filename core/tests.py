from django.shortcuts import resolve_url
from django.test import Client, TransactionTestCase

from core.models import Menu, MenuPoint


class TestMenu(TransactionTestCase):
    def setUp(self):
        """
        Create menu 'main' with the structure:

        'about'
            'about us'
                'about you'
                'about them'
        'news'
            'newspapers'

        """
        menu = Menu.objects.create(title='main')
        about = MenuPoint.objects.create(menu=menu, title='about', url_name='core:about')
        about_us = MenuPoint.objects.create(menu=menu, title='about us', url_name='core:about_us', parent=about)
        self.about_you = \
            MenuPoint.objects.create(menu=menu, title='about you', url_name='core:about_you', parent=about_us)
        MenuPoint.objects.create(menu=menu, title='about them', url_name='core:about_them', parent=about_us)

        news = MenuPoint.objects.create(menu=menu, title='news', url_name='core:news')
        MenuPoint.objects.create(menu=menu, title='newspapers', url_name='core:newspapers', parent=news)

    def test_number_queries_to_database_is_one(self):
        # No active menu point.
        with self.assertNumQueries(1):
            Client().get(resolve_url('core:index'))

        # Menu point 'about you' is active.
        with self.assertNumQueries(1):
            Client().get(resolve_url(self.about_you.url_name))
