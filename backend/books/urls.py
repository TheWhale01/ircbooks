from django.urls import path
from . import views

urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('books/', views.BooksView.as_view(), name='books'),
]