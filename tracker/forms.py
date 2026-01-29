from django import forms
from .models import CompetitionApplication, ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = [
            "full_name",
            "au_email",
            "phone_num"
        ]

class CompetitionApplicationForm(forms.ModelForm):
    class Meta:
        model = CompetitionApplication
        fields = [
            "full_name",
            "email",
            "description",
            "competition_type",
        ]
        widgets = {
            "competition_type": forms.HiddenInput(),
            "description": forms.Textarea(attrs={"maxlength": "2000",})
        }


'''
class ContactForm(forms.Form):

    full_name = forms.CharField(
        max_length=100,
        label="Full Name"
    )

    au_email = forms.EmailField(
        label="AU Email"
    )


    phone_num = forms.CharField(
        max_length=20,
        validators=[phone_regex],
        widget = forms.TextInput(attrs={
            'type': 'tel',
            'placeholder': '123-456-7890', 
            })
    )


class CompetitionApplicationForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        label = "Full Name"
    )

    email = forms.EmailField(
        label = "Email"
    )

    description = forms.CharField(
        widget=forms.Textarea,
        label = "Your major, year, why you're interested in the competition, etc."
    )
'''
