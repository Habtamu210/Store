from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from store.models import Item

@login_required
def dashboard(request):
    if request.user.groups.filter(name='Admin').exists():
        context = {
            'total_items': Item.objects.count(),
            'total_officers': User.objects.filter(groups__name='StoreOfficer').count()
        }
    else:
        context = {
            'items': Item.objects.filter(created_by=request.user)
        }
    return render(request, 'store/dashboard.html', context)
