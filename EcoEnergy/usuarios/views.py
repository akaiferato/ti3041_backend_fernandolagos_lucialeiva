from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserSignupForm
from monitoreo.models import UserOrganization, Organization


def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            organization_name = form.cleaned_data.get('organization_name')
            organization_rut = form.cleaned_data.get('organization_rut')
            organization_field = form.cleaned_data.get('organization_field')
            organization = Organization.objects.create(name=organization_name,
                                                       rut=organization_rut,
                                                       field=organization_field)

            user_organization = UserOrganization.objects.create(user=user, organization=organization)

            login(request, user)

            return redirect('monitoreo:dashboard')
    else:
        form = UserSignupForm()

    return render(request, 'signup/signup.html', {'form': form})
