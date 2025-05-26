from django.urls import path
from . import views

urlpatterns = [
    path('',views.book_list,name='book_list'),
    path('add/',views.addBook,name='addBook'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('book/<int:book_id>/edit',views.editBook,name='editBook'),
    path('book/<int:book_id>/delete',views.deleteBook,name='deleteBook'),
    path('toogle/<int:book_id>/',views.toogleStatus,name='toogleStatus'),
    
     path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
