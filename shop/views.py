import stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.http import HttpResponse
from .models import Product, Order, OrderItem
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY


def products_page(request):
    products = Product.objects.filter(is_active=True)
    paid_orders = Order.objects.filter(status="Paid").order_by("-created_at")  # 👈 YAHAN ADD KARO

    if request.method == "POST":
        total_amount = Decimal("0.00")
        cart_items = []

        # 1) Read quantities
        for p in products:
            qty = int(request.POST.get(f"qty_{p.id}", 0))
            if qty > 0:
                cart_items.append((p, qty))
                total_amount += p.price * qty

        if not cart_items:
            return render(request, "shop/products.html", {
                "products": products,
                "paid_orders": paid_orders,
                "error": "Please select at least one product."
            })

        # 2) Create Order + OrderItems (atomic)
        with transaction.atomic():
            order = Order.objects.create(total_amount=total_amount, status="Pending")
            for product, qty in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=qty
                )

        # 3) Prepare Stripe line_items (paise)
        line_items = []
        for item in order.items.all():
            line_items.append({
                "price_data": {
                    "currency": "inr",
                    "product_data": {"name": item.product.name},
                    "unit_amount": int(item.price * 100),  # ₹ -> paise
                },
                "quantity": item.quantity,
            })

        # 4) Success & Cancel URLs
        success_url = request.build_absolute_uri(
            reverse("success")
        ) + f"?order_id={order.id}&session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = request.build_absolute_uri(reverse("cancel"))

        # 5) Create Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )

        # 6) Save session id (anti double-charge)
        order.stripe_checkout_session_id = checkout_session.id
        order.save(update_fields=["stripe_checkout_session_id"])

        # 7) Redirect to Stripe
        return redirect(checkout_session.url, code=303)

    return render(request, "shop/products.html", {
        "products": products,
        "paid_orders": paid_orders  # 👈 FINAL RENDER ME PASS KARO
    })


def success(request):
    order_id = request.GET.get("order_id")
    session_id = request.GET.get("session_id")

    if not order_id or not session_id:
        messages.error(request, "Invalid payment response.")
        return redirect("products")

    order = get_object_or_404(Order, id=order_id)

    # Verify Stripe session id to avoid fake success
    if order.stripe_checkout_session_id == session_id:
        if order.status != "Paid":
            order.status = "Paid"
            order.save(update_fields=["status"])

        messages.success(
            request,
            f"Payment successful! 🎉 Order #{order.id} has been paid successfully."
        )
    else:
        messages.error(request, "Payment verification failed. Please contact support.")

    return redirect("products")


def cancel(request):
    return redirect("products")