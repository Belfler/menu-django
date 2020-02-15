from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

__all__ = ['IndexView']


class IndexView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'core/index.html')
