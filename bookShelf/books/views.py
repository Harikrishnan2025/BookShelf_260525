from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from .models import Book
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm


@login_required
def book_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')

    books = Book.objects.filter(user=request.user)
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    if status == 'read':
        books = books.filter(readORnot=True)
    elif status == 'unread':
        books = books.filter(readORnot=False)

    return render(request, 'booklist.html', {'books': books, 'query': query, 'status': status})

@login_required
def addBook(request):
    if request.method == 'POST':
        form=BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user 
            form.save()
            return redirect('book_list')
    else:
        form=BookForm()

    return render(request,'addbook.html',{'form':form})

@login_required
def editBook(request,book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    if request.method=='POST':
        form=BookForm(request.POST,instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
       form=BookForm(instance=book)
    return render (request,'editBook.html',{'form':form,'book':book})
@login_required
def deleteBook(request,book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    if request.method == "POST":
        book.delete()
        return redirect ('book_list')
    return render(request,'deletebook.html',{'book':book})


@login_required
def toogleStatus(request,book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    book.readORnot= not book.readORnot
    book.save()
    return redirect ('book_list')




def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('book_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


