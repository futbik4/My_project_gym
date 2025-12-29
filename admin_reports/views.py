from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.apps import apps
from openpyxl import Workbook
import datetime

# Проверка что пользователь - администратор
def admin_required(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(admin_required)
def export_data(request):
    """Страница выбора данных для экспорта"""
    
    # Модели которые можно экспортировать
    available_models = [
        {'name': 'Абонементы', 'app': 'core', 'model': 'Membership'},
        {'name': 'Заказы', 'app': 'core', 'model': 'Order'},
        {'name': 'Отзывы', 'app': 'core', 'model': 'Review'},
        {'name': 'Пользователи', 'app': 'auth', 'model': 'User'},
        {'name': 'Профили', 'app': 'accounts', 'model': 'Profile'},
    ]
    
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            model_path = request.POST.get('model')
            fields = request.POST.getlist('fields')
            
            if not model_path or not fields:
                messages.error(request, 'Выберите таблицу и хотя бы одно поле')
                return redirect('admin_reports:export')
            
            # Разбираем путь к модели
            app_label, model_name = model_path.split('.')
            
            # Генерируем Excel
            return generate_excel(request, app_label, model_name, fields)
            
        except Exception as e:
            messages.error(request, f'Ошибка при экспорте: {str(e)}')
            return redirect('admin_reports:export')
    
    return render(request, 'admin_reports/export.html', {
        'models': available_models
    })

def generate_excel(request, app_label, model_name, fields):
    """Генерация Excel файла с данными из модели"""
    
    # Получаем модель
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        messages.error(request, f'Модель {app_label}.{model_name} не найдена')
        return redirect('admin_reports:export')
    
    # Получаем все объекты модели
    queryset = model.objects.all()
    
    # Создаем Excel книгу
    wb = Workbook()
    ws = wb.active
    ws.title = model_name
    
    # Заголовки столбцов
    for col_num, field in enumerate(fields, 1):
        ws.cell(row=1, column=col_num, value=field)
    
    # Данные
    for row_num, obj in enumerate(queryset, 2):
        for col_num, field in enumerate(fields, 1):
            # Получаем значение поля
            value = getattr(obj, field, '')
            
            # Если поле является ForeignKey, получаем связанный объект
            if hasattr(value, 'id'):
                value = str(value)
            
            ws.cell(row=row_num, column=col_num, value=value)
    
    # Настраиваем ширину столбцов
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Сохраняем в HttpResponse
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f'{model_name}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response['Content-Disposition'] = f'attachment; filename={filename}'
    
    wb.save(response)
    return response