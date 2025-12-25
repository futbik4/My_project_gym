from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Абстрактная базовая модель с временными метками
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        abstract = True

# Модель для абонементов
class Membership(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    duration_days = models.IntegerField(verbose_name='Длительность (дней)')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    
    def __str__(self):
        return f"{self.name} - {self.price} руб."
    
    class Meta:
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'

# Модель для заказов (покупка абонемента)
class Order(TimeStampedModel):
    # Статусы заказа
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'В обработке'),
        (STATUS_COMPLETED, 'Завершен'),
        (STATUS_CANCELLED, 'Отменен'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    membership = models.ForeignKey(Membership, on_delete=models.PROTECT, verbose_name='Абонемент')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=STATUS_PENDING,
        verbose_name='Статус'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая цена')
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username} - {self.membership.name}"
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

# Модель для отзывов
class Review(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, verbose_name='Абонемент')
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Рейтинг'
    )
    comment = models.TextField(verbose_name='Комментарий')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')
    
    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.membership.name}"
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ['user', 'membership']  # Один пользователь - один отзыв на абонемент