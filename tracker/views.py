from django.shortcuts import render, redirect
from django_ratelimit.decorators import ratelimit
from .forms import ContactForm, CompetitionApplicationForm
from .models import CompetitionApplication
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .services import PortfolioService


def home(request):
    return render(request, 'home.html', {}) #we render the home page whenever the user sends a request to access the site 

def about(request):
    return render(request, 'about.html', {})

def game(request):
    return render(request, 'game.html', {"competition_type": "game"})

def cfa(request):
    return render(request, 'cfa.html', {"competition_type": "cfa"})

def college_fed(request):
    return render(request, 'college_fed.html', {"competition_type": "college_fed"})

def annual_report(request):
    return render(request, 'annual_report.html', {})

# CONTACT FORM
@ratelimit(key='ip', rate='5/h', method='POST') # 5 submissions per hour per IP for Contact Forms
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            # Phase 1: email sending will go here later

            #Set one-time success flag
            request.session["contact_submitted"] = True 
            

            # Re-render the page the user came from
            return redirect(request.META.get("HTTP_REFERER", "/"))
        
    return redirect("/")


# COMPETITION APPLICATION
@ratelimit(key='ip', rate='3/h', method='POST') # 3 submissions per hour per IP for Competition Applications
def competition_apply(request):
    if request.method != "POST":
        return redirect("/")

    # Always clear stale flags at the start of POST
    request.session.pop("competition_submitted", None)
    request.session.pop("competition_failed", None)

    appli_form = CompetitionApplicationForm(request.POST)

    if not appli_form.is_valid():
        # Re-render the same page WITH form errors
        request.session["competition_failed"] = True
        return redirect(request.META.get("HTTP_REFERER", "/"))
    
    # Check to avoid duplicate competition application submissions
    email = appli_form.cleaned_data['email'] 
    competition_type = appli_form.cleaned_data['competition_type']

    if CompetitionApplication.objects.filter(
        email = email,
        competition_type = competition_type
    ).exists():
        request.session["competition_failed"] = True
        return redirect(request.META.get('HTTP_REFERER', '/')) #end check

    application = appli_form.save(commit=False)
    application.competition_type = appli_form.cleaned_data["competition_type"]
    application.save()



    # Email to admin
    subject = f"SMIF Competition Submission: {application.full_name}"
    message = f'''
Name: {application.full_name}
Email: {application.email}
Competition: {application.get_competition_type_display()}
Description: {application.description}
        '''
    try:
        send_mail(
            subject=subject,
            message=message, 
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False, # switch to True in production to suppress errors 
        )
        #Set one-time success flag
        request.session["competition_submitted"] = True 

    except Exception as e:
        print(f"Email failed: {e}")
        request.session["competition_failed"] = True
        
    # Redirect back to the page that opened the modal
    return redirect(request.META.get("HTTP_REFERER", "/"))


def portfolio_api(request):
    """
    API endpoint that returns portfolio data as JSON
    Called by JavaScript on the frontend
    """
    service = PortfolioService()
    
    # Get portfolio data
    portfolio_result = service.get_portfolio_data()

    # Check if cache bypass is requested via query parameter
    bypass_cache = request.GET.get('bypass_cache', 'false').lower() == 'true'

    # Get portfolio data (bypass cache if requested)
    portfolio_result = service.get_portfolio_data(use_cache=not bypass_cache)
    
    # Return JSON response
    return JsonResponse({
        'portfolio': portfolio_result,
        'timestamp': portfolio_result.get('data', {}).get('last_updated') if portfolio_result.get('success') else None
    })