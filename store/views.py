from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Item
from .forms import ItemForm

@login_required
def dashboard(request):
    if request.user.groups.filter(name='Admin').exists():
        total_items = Item.objects.count()
        total_officers = User.objects.filter(groups__name='StoreOfficer').count()
        return render(request, 'store/dashboard.html', {'total_items': total_items, 'total_officers': total_officers})
    else:
        items = Item.objects.filter(created_by=request.user)
        return render(request, 'store/dashboard.html', {'items': items})

@login_required
@permission_required('store.view_item', raise_exception=True)
def item_list(request):
    items = Item.objects.all() if request.user.groups.filter(name='Admin').exists() else Item.objects.filter(created_by=request.user)
    return render(request, 'store/item_list.html', {'items': items})

@login_required
@permission_required('store.add_item', raise_exception=True)
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'store/item_form.html', {'form': form})

@login_required
@permission_required('store.change_item', raise_exception=True)
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'store/item_form.html', {'form': form})

@login_required
@permission_required('store.delete_item', raise_exception=True)
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'store/item_detail.html', {'item': item})
