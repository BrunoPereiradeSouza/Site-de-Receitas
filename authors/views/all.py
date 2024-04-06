from django.shortcuts import render, redirect
from authors.forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from authors.forms import AuthorRecipeForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    context = {'form': form, 'form_action': reverse('authors:register_create')}
    return render(request, 'authors/pages/register_view.html', context)


def register_create(request):
    if request.method != 'POST':
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in.')
        del (request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
        })


def login_create(request):
    if not request.POST:
        raise Http404
    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if authenticated_user is not None:
            messages.success(request, 'your are logged in')
            login(request, authenticated_user)
            return redirect('authors:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'invalid username or password')

    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect('authors:login')
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect('authors:login')
    logout(request)
    messages.success(request, 'logged out successfuly')
    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        author=request.user, is_published=False
    )
    return render(request, 'authors/pages/dashboard.html', context={
        'recipes': recipes
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):
    if request.method == 'POST':
        form = AuthorRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save()
            messages.success(request, 'Receita criada com sucesso!')
            return redirect(reverse('authors:dashboard'))
    else:
        form = AuthorRecipeForm()

    return render(request, 'authors/pages/dashboard_recipe.html', context={
        'form': form
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.get(
        author=request.user, is_published=False, id=id
    )

    if request.method == 'POST':
        form = AuthorRecipeForm(request.POST or None, request.FILES or None,
                                instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save()

            messages.success(request, 'Sua receita foi salva com sucesso!')
            return redirect(reverse(
                'authors:dashboard_recipe_edit', args=(id,)
                )
            )
    else:
        form = AuthorRecipeForm(instance=recipe)

    return render(request, 'authors/pages/dashboard_recipe.html', context={
        'form': form
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        recipe = Recipe.objects.get(
            author=request.user, is_published=False, id=id
        )
        recipe.delete()
        messages.success(request, 'Receita deletada com sucesso!')
    else:
        raise Http404
    return redirect(reverse('authors:dashboard'))
