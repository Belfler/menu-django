from django.shortcuts import resolve_url
from django.test import Client, TestCase

from core.models import *


class TestMenu(TestCase):
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
        self.menu = Menu.objects.create(title='main')
        self.about = MenuPoint.objects.create(menu=self.menu, title='about', url_name='core:about')
        self.about_us = MenuPoint.objects.create(menu=self.menu, title='about us',
                                                 url_name='core:about_us', parent=self.about)
        self.about_you = MenuPoint.objects.create(menu=self.menu, title='about you',
                                                  url_name='core:about_you', parent=self.about_us)
        self.about_them = MenuPoint.objects.create(menu=self.menu, title='about them',
                                                   url_name='core:about_them', parent=self.about_us)
        self.news = MenuPoint.objects.create(menu=self.menu, title='news', url_name='core:news')
        self.newspapers = MenuPoint.objects.create(menu=self.menu, title='newspapers',
                                                   url_name='core:newspapers', parent=self.news)

        self.client = Client()

    def test_number_queries_to_database_is_one(self):
        # No active menu point.
        with self.assertNumQueries(1):
            self.client.get(resolve_url('core:index'))

        # Menu point 'about you' is active.
        with self.assertNumQueries(1):
            self.client.get(resolve_url(self.about_you.url_name))
