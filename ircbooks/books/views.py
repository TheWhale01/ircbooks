from django.shortcuts import render, redirect
from django.views import View

# Create your views here.

def redirector(request):
	return (redirect('books/'))

class IndexView(View):
	def get(self, request):
		return (render(request, 'index.html'))