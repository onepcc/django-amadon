from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Q, Count, Sum

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    todas_compras= Order.objects.all().annotate(Sum('quantity_ordered'))
    gasto_total= Order.objects.all().annotate(Sum('total_price'))
    items = 0
    total = 0

    #items comprados en total
    for o in todas_compras:
        items+=o.quantity_ordered

    # suma de todas las compras en total
    for i in todas_compras:
        for s in gasto_total:
            total+= i.quantity_ordered * s.total_price

    contexto ={
            
            'todas_compras': todas_compras,
            'total': total,            
            'items': items

        }
    if request.method == "GET":
        return render(request, "store/checkout.html",contexto)
    
    if request.method == "POST":
        print(request.POST)
        quantity_from_form = int(request.POST["quantity"])
        id_from_form = request.POST["id_producto"]
        producto = Product.objects.get(id=id_from_form)
        print('precio',producto.price)

        total_charge = quantity_from_form * float(producto.price)
        print('cargo total', total_charge)
        request.session['cobro']=total_charge

        
        

        contexto ={
            'cobro':total_charge,
            'todas_compras': todas_compras,
            'gasto_total': gasto_total,
            'items': items

        }
        print("Charging credit card...")
        Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
        return redirect("/checkout/",contexto)