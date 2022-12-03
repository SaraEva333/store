from django.shortcuts import render, redirect, get_object_or_404
from .models import book, OrderItem, Order
from .forms import BookForm,UserForm, CartAddProductForm,OrderCreateForm
from django.views.generic import  DetailView, UpdateView, DeleteView, ListView
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, TemplateView, LogoutView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.decorators.http import require_POST
from .cart import Cart


def store_home(request):
    store = book.objects.all()
    paginator = Paginator(store, 2)
    cart = Cart(request)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'store/store_home.html',{'store': store,'page_obj': page_obj, 'cart': cart})

def group_required(admin):
   def in_groups(u):
       if u.is_authenticated():
           if bool(u.groups.filter(name__in=admin)) | u.is_superuser:
               return True
       return False
   return user_passes_test(in_groups)

class BLV(ListView):
        paginate_by = 2
        books = book.objects.all()
        model = book
        template_name = 'store/store_home.html'



class SDV(DetailView):
    model = book
    form = CartAddProductForm()
    template_name = 'store/d_v.html'
    context_object_name = 'article'



class SUV(PermissionRequiredMixin,UpdateView):
    permission_required = 'store.change_book'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SUV, self).dispatch(*args, **kwargs)
    model = book
    template_name = 'store/update.html'
    form_class = BookForm


class SDelV(PermissionRequiredMixin,DeleteView):
    permission_required = 'store.delete_book'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SDelV, self).dispatch(*args, **kwargs)
    model = book
    template_name = 'store/delete.html'
    success_url = '/'

@login_required
def create(request):
    error = ''
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store_home')
        else:
            error = 'Форма заполнена неверно'

    form = BookForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request,'store/create.html', data)

class LoginView(LoginView,TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                context['error'] = "Логин или пароль неправильные"
        return render(request, self.template_name, context)


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request,*args, **kwargs):
        adept_group = Group.objects.get(name='baza')
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            log = request.POST.get('log')
            password = request.POST.get('password')
            User.objects.create_user(username, email=email,first_name=log ,password=password)
            user = User.objects.get(username = username)
            user.groups.add(adept_group)
            return redirect(reverse("login"))

        return render(request, self.template_name)

class Logout(LogoutView):
    template_name = "registration/logged_out.html"
    success_url = '/'


class lk(UpdateView):
    template_name = 'registration/lk.html'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(lk, self).dispatch(*args, **kwargs)
    model = User
    user = User.objects.all()
    form_class = UserForm
    success_url = '/'

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(book, id=product_id)
    cart.add(product=product)
    # form = CartAddProductForm(request.POST)
    # if form.is_valid():
    #     cd = form.cleaned_data
    #     cart.add(product=product,
    #              quantity=cd['quantity'],
    #              update_quantity=cd['update'])
    return redirect('Cart')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(book, id=product_id)
    cart.remove(product)
    return redirect('Cart')


def cart_detail(request):
    cart = Cart(request)
    # for item in cart:
    #     item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
    #                                                                'update': True})
    return render(request, 'store/cartDetail.html', {'cart': cart})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['product'].price,
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'order/createdord.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'order/createord.html',
                  {'cart': cart, 'form': form})

def orders_check(request):
    product = book.objects.all()
    order = Order.objects.all()
    orders = OrderItem.objects.all()


    return render(request, 'order/orders.html',
                  {'orders': orders,'order': order, ' product': product})







