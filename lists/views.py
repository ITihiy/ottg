from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from lists.models import List
from lists.forms import ItemForm, ExistingListItemForm, NewListForm
User = get_user_model()


def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data={'text': request.POST['text']})
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'lists/list.html', {'list': list_, 'form': form})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(str(list_.get_absolute_url()))
    return render(request, 'lists/home.html', {'form': form})


def my_lists(request, owner):
    user = User.objects.get(email=owner)
    return render(request, 'lists/my_lists.html', {'owner': user})


def share(request, list_id):
    list_ = List.objects.get(id=list_id)
    try:
        list_.shared_with.add(User.objects.get(email=request.POST['sharee']))
    finally:
        return redirect(list_)
