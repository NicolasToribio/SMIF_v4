from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

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
    

class PortfolioHolding(models.Model):
    """
    Individual stock/ETF holding in the portfolio.
    Manage through Django Admin - add/edit/delete as you buy/sell.
    """
    ticker = models.CharField(
        max_length=10,
        unique=True,
        help_text="Stock ticker symbol (e.g., AAPL, MSFT, SPY)"
    )
    shares = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        help_text="Number of shares owned"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide from portfolio without deleting"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Portfolio Holding"
        verbose_name_plural = "Portfolio Holdings"
        ordering = ['ticker']

    def __str__(self):
        return f"{self.ticker} ({self.shares} shares)"

    def clean(self):
        """Validate ticker format before saving"""
        if self.ticker:
            self.ticker = self.ticker.upper().strip()
            if not re.match(r'^[A-Z0-9\-\.]+$', self.ticker):
                raise ValidationError({
                    'ticker': 'Ticker must contain only letters, numbers, hyphens, and periods'
                })

    def save(self, *args, **kwargs):
        """Auto-uppercase ticker before saving"""
        self.ticker = self.ticker.upper().strip()
        super().save(*args, **kwargs)