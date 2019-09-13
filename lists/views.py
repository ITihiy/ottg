from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        item = Item(text=request.POST['item_text'])
        item.save()
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'lists/home.html', {'items': Item.objects.all()})
