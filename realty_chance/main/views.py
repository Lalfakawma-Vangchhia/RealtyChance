from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Property
from django.shortcuts import get_object_or_404




# Create your views here.

def home(request):
    return render(request, 'main/index.html', {
        'title': 'Welcome to Reality Chance'
    })


def state_list(request):
    states = ["Karnataka", "Maharashtra", "Tamil Nadu", "Delhi"]
    return JsonResponse(states, safe=False)

def upload_property(request):
    if request.method == 'POST':
        Property.objects.create(
            title=request.POST['title'],
            state=request.POST['state'],
            city=request.POST['city'],
            address=request.POST['address'],
            property_type=request.POST['property_type'],
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )
        return redirect('main:dashboard')
    return render(request, 'main/upload_property.html')


def dashboard(request):
    properties = Property.objects.all()
    return render(request, 'main/dashboard.html', {'properties': properties})


def property_detail(request, id):
    property = get_object_or_404(Property, pk=id)
    return render(request, 'main/property_detail.html', {'property': property})

