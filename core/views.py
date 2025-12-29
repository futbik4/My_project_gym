from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Membership, Order, Review

def home(request):
    return render(request, 'core/index.html')

def services(request):
    return render(request, 'core/services.html')

def news(request):
    return render(request, 'core/news.html')

def contacts(request):
    return render(request, 'core/contacts.html')

def pageN(request):
    return render(request, 'core/pageN.html')

def memberships_list(request):
    """Страница со списком абонементов с поиском"""
    query = request.GET.get('q', '')
    memberships = Membership.objects.filter(is_active=True)
    
    if query:
        memberships = memberships.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    return render(request, 'core/memberships.html', {
        'memberships': memberships,
        'query': query
    })

@login_required
def create_order(request, membership_id):
    """Создание заказа (покупка абонемента)"""
    # Проверка - если имя пользователя 'guest'
    if request.user.username == 'guest':
        messages.error(request, 'Гость не может покупать абонементы. Зарегистрируйтесь!')
        return redirect('accounts:register')
    
    membership = get_object_or_404(Membership, id=membership_id, is_active=True)
    
    # Если пользователь уже покупал этот абонемент
    existing_order = Order.objects.filter(
        user=request.user, 
        membership=membership,
        status=Order.STATUS_COMPLETED
    ).exists()
    
    if existing_order:
        messages.warning(request, f'У вас уже есть активный абонемент "{membership.name}"')
        return redirect('core:memberships')
    
    if request.method == 'POST':
        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            membership=membership,
            total_price=membership.price,
            status=Order.STATUS_PENDING
        )
        messages.success(request, f'Заказ #{order.id} успешно оформлен! Статус: {order.get_status_display()}')
        return redirect('core:order_detail', order_id=order.id)
    
    return render(request, 'core/create_order.html', {
        'membership': membership,
        'existing_order': existing_order
    })

@login_required
def order_detail(request, order_id):
    """Детальная информация о заказе"""
    # Проверка на гостя
    if request.user.username == 'guest':
        messages.error(request, 'Гость не имеет доступа к заказам')
        return redirect('core:home')
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})

@login_required
def my_orders(request):
    """Страница с заказами пользователя"""
    # Проверка на гостя
    if request.user.username == 'guest':
        messages.info(request, 'У гостя нет истории заказов')
        return redirect('core:home')
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/my_orders.html', {'orders': orders})

def membership_reviews(request, membership_id):
    """Отзывы на конкретный абонемент"""
    membership = get_object_or_404(Membership, id=membership_id)
    reviews = Review.objects.filter(membership=membership, is_approved=True)
    
    return render(request, 'core/membership_reviews.html', {
        'membership': membership,
        'reviews': reviews
    })

@login_required
def add_review(request, membership_id):
    """Добавление отзыва к абонементу"""
    membership = get_object_or_404(Membership, id=membership_id)
    
    # Проверяем, есть ли у пользователя завершенный заказ этого абонемента
    has_order = Order.objects.filter(
        user=request.user,
        membership=membership,
        status=Order.STATUS_COMPLETED
    ).exists()
    
    if not has_order:
        messages.error(request, 'Вы можете оставить отзыв только после покупки абонемента')
        return redirect('core:membership_reviews', membership_id=membership_id)
    
    # Проверяем, не оставлял ли уже отзыв
    existing_review = Review.objects.filter(user=request.user, membership=membership).first()
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        
        if not rating:
            messages.error(request, 'Пожалуйста, выберите оценку')
        elif not comment:
            messages.error(request, 'Пожалуйста, напишите комментарий')
        else:
            if existing_review:
                # Обновляем существующий отзыв
                existing_review.rating = rating
                existing_review.comment = comment
                existing_review.is_approved = False  # Требует повторной модерации
                existing_review.save()
                messages.success(request, 'Отзыв обновлен и отправлен на модерацию')
            else:
                # Создаем новый отзыв
                Review.objects.create(
                    user=request.user,
                    membership=membership,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, 'Отзыв добавлен и отправлен на модерацию')
            
            return redirect('core:membership_reviews', membership_id=membership_id)
    
    return render(request, 'core/add_review.html', {
        'membership': membership,
        'existing_review': existing_review
    })