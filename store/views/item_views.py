from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from store.models import Item
from store.forms import ItemForm


@login_required
@permission_required('store.view_item', raise_exception=True)
def item_list(request):
    user = request.user

    if user.groups.filter(name='Admin').exists():
        items = Item.objects.all()
    else:
        items = Item.objects.filter(created_by=user)

    return render(request, 'store/items/list.html', {'items': items})


@login_required
@permission_required('store.add_item', raise_exception=True)
def item_create(request):
    form = ItemForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.created_by = request.user
        item.save()
        return redirect('item_list')

    return render(request, 'store/items/form.html', {'form': form})


@login_required
@permission_required('store.change_item', raise_exception=True)
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Officers may only edit their own items
    if request.user.groups.filter(name='StoreOfficer').exists() and item.created_by != request.user:
        return redirect('item_list')

    form = ItemForm(request.POST or None, instance=item)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('item_list')

    return render(request, 'store/items/form.html', {'form': form})


@login_required
@permission_required('store.delete_item', raise_exception=True)
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Officers may only delete their own items
    if request.user.groups.filter(name='StoreOfficer').exists() and item.created_by != request.user:
        return redirect('item_list')

    if request.method == 'POST':
        item.delete()
        return redirect('item_list')

    return render(request, 'store/items/delete.html', {'item': item})
