from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
import json

# Create your views here.
def redirector(request):
	return (redirect('books/'))

class IndexView(View):
	def get(self, request):
		return (render(request, 'index.html'))

	def post(self, request):
		request_body = request.body.decode()
		if (not request_body):
			return (JsonResponse({'message': 'No body found.'}))
		body = json.loads(request_body);
		request.session['nickname'] = body['nickname']
		return (redirect('books/'))

class BooksView(View):
	def get(self, request):
		if ('nickname' not in request.session):
			return (redirect(''))
		return (render(request, 'books.html', {
			'nickname': request.session['nickname'],
		}))