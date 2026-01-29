from .forms import ContactForm

def contact_form(request):
    return {
        "form": ContactForm()
    }

def contact_submission_flag(request):
    return {
        "contact_submitted": request.session.pop("contact_submitted", False)
    }

def competition_submission_flag(request):
    return {
        "competition_submitted": request.session.pop("competition_submitted", False)
    }

def competition_failed_flag(request):
    return {
        "competition_failed": request.session.pop("competition_failed", False)
    }