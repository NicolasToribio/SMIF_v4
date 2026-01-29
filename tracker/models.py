from django.db import models
from django.core.validators import RegexValidator

phone_regex = RegexValidator( #Used to validate phone numbers 
    regex=r'^\+?1?\D*(\d\D*){10}$',
    message = "Enter a valid US phone number."
)


class ContactSubmission(models.Model):
    full_name = models.CharField(max_length=100)
    au_email = models.EmailField()
    phone_num = models.CharField(
        max_length=20,
        validators=[phone_regex]
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Redefining name, overriding default
    class Meta:
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"Contact: {self.full_name} ({self.au_email})"


class CompetitionApplication(models.Model):
    COMPETITION_CHOICES = [
        ("college_fed", "College Fed"),
        ("cfa", "CFA"),
        ("game", "Game"),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField(max_length=2000)
    competition_type = models.CharField(
        max_length = 50,
        choices = COMPETITION_CHOICES
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Redefining name, overriding default
    class Meta:
        verbose_name = "Competition Application"
        verbose_name_plural = "Competition Applications"


    def __str__(self):
        return f"Application: {self.full_name} - {self.get_competition_type_display()}"