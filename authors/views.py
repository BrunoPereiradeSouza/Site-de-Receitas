from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import Http404


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    context = {'form': form}
    return render(request, 'authors/pages/register_view.html', context)


def register_create(request):
    if request.method != 'POST':
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    return redirect('authors:register')

