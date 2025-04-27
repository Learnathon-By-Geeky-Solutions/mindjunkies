from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from mindjunkies.dashboard.models import TeacherVerification


class VerifiedTeacherRequiredMixin(LoginRequiredMixin):
    """
    Mixin to ensure the user is a verified teacher.
    Redirects to verification wait page or teacher application form if not.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')

        if not request.user.is_teacher:
            return redirect('teacher_permission')

        try:
            verification = TeacherVerification.objects.get(user=request.user)
            if not verification.verified:
                return redirect('verification_wait')
        except TeacherVerification.DoesNotExist:
            return redirect('teacher_permission')

        return super().dispatch(request, *args, **kwargs)
