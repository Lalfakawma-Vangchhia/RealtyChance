from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ListedProperty
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import UserProfile


def home(request):
    properties = ListedProperty.objects.all()
    return render(request, 'main/index.html', {
        'title': 'Welcome to Reality Chance',
        'properties': properties
    })


def state_list(request):
    states = ["Karnataka", "Maharashtra", "Tamil Nadu", "Delhi"]
    return JsonResponse(states, safe=False)


def upload_property(request):
    amenities = [
        'Air Conditioning', 'Balcony', 'Garage', 'Gym',
        'Swimming Pool', 'Furnished', 'Pet Friendly', 'Security',
        'Garden', 'Elevator', 'Parking', 'Internet'
    ]
    if request.method == 'POST':
        ListedProperty.objects.create( 
            user=request.user,
            title=request.POST['title'],
            state=request.POST['state'],
            city=request.POST['city'],
            address=request.POST['address'],
            property_type=request.POST['property_type'],
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )
        return redirect('main:my_properties')
    return render(request, 'main/upload_property.html', {'amenities': amenities})



@login_required
def my_properties(request):
    properties = ListedProperty.objects.filter(user=request.user).order_by('-listed_on')
    return render(request, 'main/my_properties.html', {'properties': properties})


def property_detail(request, id):
    property = get_object_or_404(ListedProperty, pk=id)
    return render(request, 'main/property_detail.html', {'property': property})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            UserProfile.objects.create(user=user, role=role)
            return redirect('main:login')  # or 'main:home'
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})


