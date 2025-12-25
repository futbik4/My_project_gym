from django.shortcuts import render

def export_data(request):
    return render(request, 'admin_reports/export.html')