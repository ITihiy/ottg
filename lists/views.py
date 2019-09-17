from django.shortcuts import render, redirect

from lists.models import Item, List


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request):
    return render(request, 'lists/list.html', {'items': Item.objects.all()})


def new_list(request):
    Item.objects.create(text=request.POST['item_text'], list=List.objects.create())
    return redirect('/lists/the-only-list-in-the-world/')
