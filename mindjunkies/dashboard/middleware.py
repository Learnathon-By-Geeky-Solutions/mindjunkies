from django.shortcuts import redirect
from django.urls import reverse

class TeacherVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Exclude the teacher verification form from the restriction
        teacher_verification_url = reverse('teacher_verification_form')  # Get the actual URL pattern
        
        if request.path.startswith('/teacher/') and request.path != teacher_verification_url:
            if not getattr(request.user, 'is_teacher', False):
                return redirect(teacher_verification_url)

        return self.get_response(request)