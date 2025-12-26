# core/middleware.py
class GuestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Если пользователь гость, устанавливаем флаг в сессии
        if request.user.is_authenticated and request.user.username == 'guest_user':
            request.session['is_guest'] = True
            print(f"DEBUG: User {request.user.username} is guest")
        else:
            request.session['is_guest'] = False
            
        response = self.get_response(request)
        return response