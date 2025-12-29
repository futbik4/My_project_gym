# core/admin_actions.py
import datetime
from django.http import HttpResponse
from django.contrib import messages
from openpyxl import Workbook

def export_as_xlsx(modeladmin, request, queryset):
    """Экспорт выбранных объектов в Excel"""
    
    # Создаем Excel книгу
    wb = Workbook()
    ws = wb.active
    ws.title = modeladmin.model.__name__
    
    # Получаем все поля модели
    model = modeladmin.model
    field_names = [field.name for field in model._meta.fields]
    
    # Заголовки
    ws.append(field_names)
    
    # Данные
    for obj in queryset:
        row = []
        for field_name in field_names:
            value = getattr(obj, field_name)
            if hasattr(value, '__str__'):
                row.append(str(value))
            else:
                row.append(value)
        ws.append(row)
    
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
        adjusted_width = min(max_length + 2, 30)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Создаем HTTP ответ
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f'{model.__name__}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    wb.save(response)
    
    messages.success(request, f'Экспортировано {queryset.count()} записей')
    return response

export_as_xlsx.short_description = "Экспорт выбранных записей в Excel"