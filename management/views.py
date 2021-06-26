from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from authentication.decorators import dealer_employee_required, dealer_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.http import QueryDict
from django.db.models.functions import TruncMonth, TruncYear, TruncDay, TruncDate
from django.db.models import Sum, Count
from django.urls import reverse
import pytz
from django.http import JsonResponse

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML
import json

# ================
# Inner app module
# ================
from orderangel import settings
from .forms import EmployeeCreationForm, EmployeeChangeForm, ProductCreationForm, ProductChangeForm, CategoryCUForm, \
    SettingForm
from .models import Employee, Product, Category, Settings, Order, Invoice, PriceUnit
from authentication.models import Client
from .serializers import EmployeeSerializer, ProductSerializer, InvoicesSerializer, InvoicesClientSerializer
from .utils import InvoiceState, createInvoice


def home(request):
    setting = Settings.objects.filter(pk=1).first()
    categories = Category.objects.filter(is_active=True).all()

    return render(request, "public/profile.html", {'user': request.user,
                                                   'categories': categories,
                                                   'setting': setting})


def cart(request):
    if request.method == "POST":
        response = HttpResponse(status=200)
        key = "productcart" + str(request.POST.get("product")) + str(request.POST.get("unit"))
        response.set_cookie(key, json.dumps(request.POST.dict()))
        return response

    if request.method == "GET":
        result = dict()
        for key in request.COOKIES.keys():
            if key.startswith("productcart"):
                result[key] = json.loads(request.COOKIES[key])

        return JsonResponse({
            "count": len(result),
            "result": result
        })


########################################################################################################################
#                                                                                                                      #
#                                    Home Views                                                                        #
#                                                                                                                      #
########################################################################################################################


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_account(request):
    return render(request, 'dashboard/secure_home.html',
                  {'user': request.user})


########################################################################################################################
#                                                                                                                      #
#                                    Client Views                                                                      #
#                                                                                                                      #
########################################################################################################################


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_clients(request):
    return render(request, 'dashboard/secure_clients.html',
                  {'user': request.user})


@api_view(['GET'])
def secure_clients_data_table(request):
    order_position = "" if request.GET.get("order[0][dir]", "asc") == 'asc' else "-"
    position_from = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    if request.GET.get("search[value]", False):
        clients = Invoice.objects.exclude(
            ~Q(client__company_name__istartswith=request.GET["search[value]"]) & ~Q(
                client__first_name__istartswith=request.GET["search[value]"]) & ~Q(
                client__last_name__istartswith=request.GET["search[value]"])) \
            .order_by(order_position + "client__company_name").distinct('client', 'client__company_name')
    else:
        clients = Invoice.objects.all().order_by(order_position + "client__company_name") \
            .distinct('client',
                      'client__company_name')

    records_total = clients.count()

    paginator = Paginator(clients, length)
    page_id = (position_from // paginator.per_page) + 1
    if page_id > paginator.num_pages:
        page_id = paginator.num_pages
    elif page_id < 1:
        page_id = 1

    try:
        pr = paginator.page(page_id)
    except PageNotAnInteger:
        pr = paginator.page(1)
    except EmptyPage:
        pr = paginator.page(paginator.num_pages)

    serializer = InvoicesClientSerializer(pr, many=True)

    return Response({
        "recordsTotal": records_total,
        "recordsFiltered": records_total,
        "results": serializer.data
    })


########################################################################################################################
#                                                                                                                      #
#                                    Setting Views                                                                     #
#                                                                                                                      #
########################################################################################################################

@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_settings(request):
    setting = Settings.objects.filter(pk=1).first()
    form = SettingForm(request.GET or None, instance=setting)
    if request.method == "POST":
        form = SettingForm(request.POST, request.FILES, instance=setting)
        if form.is_valid():
            form.save(commit=True)
    return render(request, 'dashboard/secure_settings.html',
                  {'user': request.user, 'form': form})


########################################################################################################################
#                                                                                                                      #
#                                    Category Views                                                                    #
#                                                                                                                      #
########################################################################################################################

@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_categories(request):
    return render(request, 'dashboard/secure_categories.html',
                  {'user': request.user, 'categories': Category.objects.all()})


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_category_profile(request, id):
    category = get_object_or_404(Category, pk=id)
    form = CategoryCUForm(request.POST or None, instance=category)
    if request.method == "POST":
        form = CategoryCUForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category.save()

    return render(request, 'dashboard/secure_category_creation.html',
                  {'user': request.user, 'form': form})


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_category_creation(request):
    if request.method == "POST":
        form = CategoryCUForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.is_active = True
            category.save()
            return redirect(secure_categories)
        return render(request, 'dashboard/secure_category_creation.html',
                      {'user': request.user, 'form': form})
    return render(request, 'dashboard/secure_category_creation.html',
                  {'user': request.user, 'form': CategoryCUForm()})


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_category_products(request, cid):
    return secure_products(request, cid=cid)


########################################################################################################################
#                                                                                                                      #
#                                    Order Views                                                                       #
#                                                                                                                      #
########################################################################################################################

@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_orders(request):
    if request.META['REQUEST_METHOD'] == 'DELETE':
        if QueryDict(request.body).get("invoice", None):
            invoice = get_object_or_404(Invoice, pk=QueryDict(request.body).get("invoice", None), is_active=1)
            invoice.is_active = False
            invoice.save()
            for order in invoice.get_active_orders():
                order.is_active = False
                order.save()
            return HttpResponse(status=200)

    if request.method == 'POST':
        ids = request.POST.getlist("ids[]", None)
        if ids:
            for ix, id in enumerate(ids):
                if ix == 0:
                    target_invoice = Invoice.objects.get(pk=id)
                else:
                    invoice = Invoice.objects.get(pk=id)
                    if invoice.client.id == target_invoice.client.id:
                        for order in invoice.order_set.all():
                            order.invoice = target_invoice
                            order.save()
                        invoice.is_active = False
                        invoice.save()
            return HttpResponse(status=200)
    return render(request, 'dashboard/secure_orders.html',
                  {'user': request.user, 'states': InvoiceState.states})


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_invoice_profile(request, id):
    invoice = Invoice.objects.filter(pk=id, is_active=1).first()
    setting = Settings.objects.filter(pk=1).first()
    if request.method == "POST":
        product = get_object_or_404(Product, pk=request.POST.get("product"))
        unit = product.priceunit_set.filter(is_active=True, name=request.POST.get("unit")).first()
        order = invoice.order_set.filter(product__pk=request.POST.get("product"),
                                         units=request.POST.get("unit"),
                                         is_active=1).first()
        if order:
            order.amount = float(order.amount) + float(request.POST.get("amount"))
        else:
            order = Order()
            order.product = product
            order.invoice = invoice
            order.units = request.POST.get("unit")
            order.price = unit.price
            order.amount = request.POST.get("amount")
        order.save()

    return render(request, 'dashboard/secure_invoice_profile.html',
                  {'user': request.user, 'settings': setting, 'invoice': invoice})


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_invoice_download(request, id):
    invoice = Invoice.objects.filter(uuid=id, is_active=1).first()
    setting = Settings.objects.filter(pk=1).first()

    html_string = render_to_string('dashboard/pdf_template.html',
                                   {
                                       'invoice': invoice,
                                       'settings': setting,
                                       'open_when': [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                                       'close_when': list(range(9, 100, 10)),
                                   })

    html = HTML(string=html_string,
                encoding='utf-8',
                base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/' + id + '.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('/tmp/' + id + '.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + id + '.pdf"'
        return response


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_orders_profile(request, id):
    invoice = Invoice.objects.filter(pk=id, is_active=1).first()
    return render(request, 'dashboard/secure_orders_profile.html',
                  {'user': request.user, 'invoice': invoice})


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def create_order(request):
    if request.method == 'POST':
        if request.POST.get("client", None):
            invoice = Invoice()
            invoice.client = get_object_or_404(Client, pk=request.POST.get("client"))
            invoice.uuid = createInvoice(invoice.client.pk)
            invoice.state = InvoiceState.states[request.POST.get("state")]
            invoice.issue_date = datetime.strptime(request.POST.get("date"), "%d/%m/%Y %H:%M").astimezone(
                tz=pytz.timezone("Europe/Berlin"))
            invoice.save(force_insert=True)
            invoice.save()
            return redirect(reverse('secure.invoice.profile', kwargs={'id': invoice.pk}))
    return HttpResponse(status=200)


@api_view(['POST', 'DELETE'])
def update_orders(request):
    if request.META['REQUEST_METHOD'] == "DELETE":
        request.DELETE = QueryDict(request.body)
        order = get_object_or_404(Order, pk=request.DELETE.get("order_id"))
        order.is_active = False
        order.save()
    if request.method == 'POST':
        for id in request.POST.getlist("ids[]"):
            invoice = Invoice.objects.get(pk=id)
            invoice.state = InvoiceState.states.get(request.POST.get("state"), 0)
            invoice.save()
    return HttpResponse(status=200)


@api_view(['GET'])
def secure_invoices_data_table(request):
    if request.method == 'GET':
        order_column = int(request.GET.get("order[0][column]", 5))
        order_position = "" if request.GET.get("order[0][dir]", "asc") == 'asc' else "-"
        position_from = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        if request.GET.get("search[value]", False):
            invoices = Invoice.objects.filter(
                (Q(uuid__istartswith=request.GET["search[value]"]) | Q(
                    client__company_name__istartswith=request.GET["search[value]"]) | Q(
                    client__first_name__istartswith=request.GET["search[value]"]) | Q(
                    client__last_name__istartswith=request.GET["search[value]"])
                 ) & Q(is_active=True)) \
                .order_by(order_position + InvoicesSerializer.Meta.ordering[order_column])

        else:
            invoices = Invoice.objects.filter(is_active=True).order_by(
                order_position + InvoicesSerializer.Meta.ordering[order_column])

        records_total = invoices.count()

        # paginator
        paginator = Paginator(invoices, length)
        page_id = (position_from // paginator.per_page) + 1
        if page_id > paginator.num_pages:
            page_id = paginator.num_pages
        elif page_id < 1:
            page_id = 1

        try:
            pr = paginator.page(page_id)
        except PageNotAnInteger:
            pr = paginator.page(1)
        except EmptyPage:
            pr = paginator.page(paginator.num_pages)

        serializer = InvoicesSerializer(pr, many=True)

        return Response({
            "recordsTotal": records_total,
            "recordsFiltered": records_total,
            "results": serializer.data
        })


@api_view(['GET'])
def secure_invoices_data_table_product(request):
    if request.method == 'GET':
        order_column = int(request.GET.get("order[0][column]", 5))
        order_position = "" if request.GET.get("order[0][dir]", "asc") == 'asc' else "-"
        position_from = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        if request.GET.get("search[value]", False):
            invoices = Invoice.objects.filter(
                (Q(uuid__istartswith=request.GET["search[value]"]) | Q(
                    client__company_name__istartswith=request.GET["search[value]"]) | Q(
                    client__first_name__istartswith=request.GET["search[value]"]) | Q(
                    client__last_name__istartswith=request.GET["search[value]"])
                 ) & Q(is_active=True) & Q(order__product__pk=1)) \
                .order_by(order_position + InvoicesSerializer.Meta.ordering[order_column])

        else:
            invoices = Invoice.objects.filter(
                Q(is_active=True) & Q(order__product__pk=int(request.GET.get("product-id", 0)))).order_by(
                order_position + InvoicesSerializer.Meta.ordering[order_column])

        records_total = invoices.count()

        # paginator
        paginator = Paginator(invoices, length)
        page_id = (position_from // paginator.per_page) + 1
        if page_id > paginator.num_pages:
            page_id = paginator.num_pages
        elif page_id < 1:
            page_id = 1

        try:
            pr = paginator.page(page_id)
        except PageNotAnInteger:
            pr = paginator.page(1)
        except EmptyPage:
            pr = paginator.page(paginator.num_pages)

        serializer = InvoicesSerializer(pr, many=True)

        return Response({
            "recordsTotal": records_total,
            "recordsFiltered": records_total,
            "results": serializer.data
        })


########################################################################################################################
#                                                                                                                      #
#                                    Statistic Views                                                                   #
#                                                                                                                      #
########################################################################################################################

@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_statistics(request):
    return render(request, 'dashboard/secure_statistic.html',
                  {'user': request.user})


########################################################################################################################
#                                                                                                                      #
#                                    Product Views                                                                     #
#                                                                                                                      #
########################################################################################################################

@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_products(request, cid=0):
    return render(request, 'dashboard/secure_products.html',
                  {'user': request.user, 'category': cid})


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_product_creation(request):
    if request.method == "POST":
        form = ProductCreationForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if form["offer_period"].value() != "":
                offers = form["offer_period"].value().split("-")
                product.offer_start = datetime.strptime(offers[0].strip(), '%d/%m/%Y')
                product.offer_end = datetime.strptime(offers[1].strip(), '%d/%m/%Y')
            product.is_active = True
            product.save()
            return redirect(secure_product_profile, id=product.pk)
        return render(request, 'dashboard/secure_product_creation.html',
                      {'user': request.user, 'form': form})
    return render(request, 'dashboard/secure_product_creation.html',
                  {'user': request.user, 'form': ProductCreationForm()})


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_product_pricing(request):
    if request.method == "GET":

        if request.GET.get('id', None):
            prices = PriceUnit.objects.filter(product=request.GET.get('id'), is_active=True).all()
            data = dict()
            for price in prices:
                data[price.name] = price.get_name_display()
            return JsonResponse({'result': data}, safe=False, content_type='application/json')

    if request.META['REQUEST_METHOD'] == "DELETE":
        request.DELETE = QueryDict(request.body)
        if request.DELETE.get('id', None):
            units = PriceUnit.objects.get(pk=request.DELETE.get('id'))
            units.is_active = False
            units.save()
        return HttpResponse(status=200)

    if request.method == "POST":
        product = get_object_or_404(Product, pk=request.POST.get("id"))
        price_unit = {}
        for i in range(0, len(request.POST)):
            if len(request.POST.getlist("repeater-group[" + str(i) + "][units]")) > 0:
                price_unit[request.POST.getlist("repeater-group[" + str(i) + "][units]")[0]] = request.POST.getlist(
                    "repeater-group[" + str(i) + "][price]")[0]
        for k_unit, price in price_unit.items():
            unit = product.priceunit_set.filter(
                name=k_unit, is_active=True).first()
            if unit:
                if price:
                    unit.price = price
                else:
                    unit.price = None
            else:
                unit = PriceUnit()
                unit.product = product
                unit.name = k_unit
                if price:
                    unit.price = price
            unit.save()
        return redirect(reverse('secure.product.profile', kwargs={'id': request.POST.get("id")}))


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_product_profile(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductChangeForm(request.POST or None, instance=product)
    # Set product period of offer
    form.fields["offer_period"].initial = '%s - %s' % (
        product.offer_start.strftime("%d/%m/%Y"), product.offer_end.strftime("%d/%m/%Y")) if product.offer_end else ""
    # handle post request (update)
    if request.method == "POST":
        form = ProductChangeForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            if form["offer_period"].value() != "":
                offers = form["offer_period"].value().split("-")
                product.offer_start = datetime.strptime(offers[0].strip(), '%d/%m/%Y')
                product.offer_end = datetime.strptime(offers[1].strip(), '%d/%m/%Y')

            product.save()

        else:
            print(form.errors)
    return render(request, 'dashboard/secure_product_profile.html',
                  {'user': request.user, 'form': form, 'id': id})


@login_required(login_url=settings.LOGIN_URL)
@dealer_required(login_url=settings.LOGIN_URL)
def secure_product_update(request):
    """
    Delete product image or update product state
    :param request:
    :return: state
    """
    # delete product
    if request.META['REQUEST_METHOD'] == "DELETE":
        request.DELETE = QueryDict(request.body)
        product = get_object_or_404(Product, pk=int(request.DELETE.get("product_id")))
        product.image = ""
        product.save()
        return HttpResponse(status=200)

    # update product state
    if request.method == "POST":
        product = get_object_or_404(Product, pk=int(request.POST.get("product_id")))
        product.is_active = not product.is_active
        product.save()
        return HttpResponse(status=200)
    return HttpResponse(status=404)


@api_view(['GET'])
def prices(request):
    if request.method == "GET":

        if request.GET.get('id', None):
            prices = PriceUnit.objects.filter(product=request.GET.get('id'), is_active=True).all()
            data = dict()
            for price in prices:
                data[price.name] = {
                    "name": price.get_name_display(),
                    "price": price.price
                }

            return JsonResponse({'result': data}, safe=False, content_type='application/json')


@api_view(['GET'])
def secure_products_data_table(request):
    if request.method == 'GET':
        order_column = int(request.GET.get("order[0][column]", 0))
        order_position = "" if request.GET.get("order[0][dir]", "asc") == 'asc' else "-"
        position_from = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        category = int(request.GET.get("cid")) if request.GET.get("cid") else 0
        if request.GET.get("search[value]", False):
            if category > 0:
                products = Product.objects.filter(((Q(article_number__istartswith=request.GET["search[value]"]) | Q(
                    name__istartswith=request.GET["search[value]"])) & Q(
                    category__id=category))) \
                    .order_by(order_position + ProductSerializer.Meta.ordering[order_column])

            else:
                products = Product.objects.filter((Q(article_number__istartswith=request.GET["search[value]"]) | Q(
                    name__istartswith=request.GET["search[value]"]) | Q(
                    category__name__istartswith=request.GET["search[value]"]))) \
                    .order_by(order_position + ProductSerializer.Meta.ordering[order_column])
        else:
            if category > 0:
                products = Product.objects.filter(category__id=category).order_by(
                    order_position + ProductSerializer.Meta.ordering[order_column])
            else:
                products = Product.objects.order_by(
                    order_position + ProductSerializer.Meta.ordering[order_column]).all()

        # count records total
        records_total = products.count()

        # paginator
        paginator = Paginator(products, length)
        page_id = (position_from // paginator.per_page) + 1
        if page_id > paginator.num_pages:
            page_id = paginator.num_pages
        elif page_id < 1:
            page_id = 1

        try:
            pr = paginator.page(page_id)
        except PageNotAnInteger:
            pr = paginator.page(1)
        except EmptyPage:
            pr = paginator.page(paginator.num_pages)

        serializer = ProductSerializer(pr, many=True)

        return Response({
            "recordsTotal": records_total,
            "recordsFiltered": records_total,
            "results": serializer.data
        })


@api_view(['GET'])
def secure_products_statistics(request):
    if request.method == "GET":
        if request.GET.get("type") == "TotalOrders":
            result = Invoice.objects.filter(order__product=request.GET.get("product"),
                                            is_active=True).count()
            return Response({
                "result": result,
            })
        if request.GET.get("type") == "SumOrders":
            result = Invoice.objects.filter(order__product=request.GET.get("product"),
                                            is_active=True).aggregate(sum=Sum('order__amount'))
            return Response({
                "result": result["sum"],
            })

        if request.GET.get("from", None):
            date_from = datetime.strptime(request.GET.get("from"), '%d-%m-%Y') - timedelta(days=1)
            date_till = datetime.strptime(request.GET.get("till"), '%d-%m-%Y') + timedelta(days=1)
        else:
            date_from = datetime.now() + timedelta(days=-14)
            date_till = datetime.now()

        if request.GET.get("interval") == "Monthly":
            result = Invoice.objects.filter(created_date__range=[date_from, date_till],
                                            order__product=request.GET.get("product"),
                                            is_active=True).annotate(
                month=TruncMonth('created_date')).values('month').annotate(count=Count('id')).values('month', 'count')
        elif request.GET.get("interval") == "Daily":
            result = Invoice.objects.filter(created_date__range=[date_from, date_till],
                                            order__product=request.GET.get("product"),
                                            is_active=True).annotate(
                day=TruncDay('created_date')).values('day').annotate(count=Count('id')).values('day', 'count')
        else:
            result = Invoice.objects.filter(created_date__range=[date_from, date_till],
                                            order__product=request.GET.get("product"),
                                            is_active=True).annotate(
                year=TruncYear('created_date')).values('year').annotate(count=Count('id')).values('year', 'count')

        return Response({
            "result": result,
        })


########################################################################################################################
#                                                                                                                      #
#                                    Employee Views                                                                    #
#                                                                                                                      #
########################################################################################################################

@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_employees(request):
    return render(request, 'dashboard/secure_employees.html',
                  {'user': request.user})


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_employee_creation(request):
    if request.method == "POST":
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.password = make_password(form.cleaned_data["password"])
            employee.save()
            return redirect(secure_employee_profile, id=employee.pk)
        return render(request, 'dashboard/secure_employee_creation.html',
                      {'user': request.user, 'form': form})

    return render(request, 'dashboard/secure_employee_creation.html',
                  {'user': request.user, 'form': EmployeeCreationForm()})


@login_required(login_url=settings.LOGIN_URL)
@dealer_required(login_url=settings.LOGIN_URL)
def secure_employee_update(request):
    if request.method == "POST":
        employee = get_object_or_404(Employee, pk=int(request.POST.get("employee_id")))
        employee.is_active = not employee.is_active
        employee.save()
        return HttpResponse(status=200)
    return HttpResponse(status=404)


@login_required(login_url=settings.LOGIN_URL)
@dealer_employee_required(login_url=settings.LOGIN_URL)
def secure_employee_profile(request, id):
    employee = get_object_or_404(Employee, pk=id)
    form = EmployeeChangeForm(request.POST or None, instance=employee)
    if request.method == "POST":
        print(form.errors)
        if form.is_valid():
            if form.cleaned_data["password2"] == "":
                form.password = employee.password
            else:
                form.password = make_password(form.cleaned_data["password2"])
            form.save()

    return render(request, 'dashboard/secure_employee_profile.html',
                  {'user': request.user, 'form': form, 'target_user_pk': id})


@api_view(['GET'])
def secure_employee_data_table(request):
    if request.method == 'GET':
        order_column = int(request.GET.get("order[0][column]", 0))
        order_position = "" if request.GET.get("order[0][dir]", "asc") == 'asc' else "-"
        position_from = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        if request.GET.get("search[value]", False):
            employees = Employee.objects.filter(Q(email__istartswith=request.GET["search[value]"]) | Q(
                first_name__istartswith=request.GET["search[value]"]) | Q(
                last_name__istartswith=request.GET["search[value]"]) | Q(
                position__istartswith=request.GET["search[value]"])) \
                .order_by(order_position + EmployeeSerializer.Meta.ordering[order_column])
        else:
            employees = Employee.objects.order_by(order_position + "pk").all()

        # count records total
        records_total = employees.count()

        # paginator
        paginator = Paginator(employees, length)
        page_id = (position_from // paginator.per_page) + 1
        if page_id > paginator.num_pages:
            page_id = paginator.num_pages
        elif page_id < 1:
            page_id = 1

        try:
            em = paginator.page(page_id)
        except PageNotAnInteger:
            em = paginator.page(1)
        except EmptyPage:
            em = paginator.page(paginator.num_pages)

        serializer = EmployeeSerializer(em, many=True)

        return Response({
            "recordsTotal": records_total,
            "recordsFiltered": records_total,
            "results": serializer.data
        })
