from django.db import models

# Create your models here.

class Company(models.Model):
    symbol = models.CharField(unique=True, max_length=10, null=True, blank=True)
    LTP = models.CharField(max_length=10, null=True, blank=True)
    pt_change = models.CharField(max_length=10, null=True, blank=True)
    percentage_change = models.CharField(max_length=10, null=True, blank=True)
    added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.symbol

class CompanyDetail(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    sector = models.CharField(max_length=255, null=True, blank=True)
    permitted_to_trade = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    as_of = models.CharField(max_length=255, null=True, blank=True)
    instrument_type = models.CharField(max_length=255, null=True, blank=True)
    listing_date = models.CharField(max_length=255, null=True, blank=True)
    last_traded_price = models.CharField(max_length=255, null=True, blank=True)
    total_traded_quantity = models.CharField(max_length=255, null=True, blank=True)
    total_trades = models.CharField(max_length=255, null=True, blank=True)
    previous_day_close_price = models.CharField(max_length=255, null=True, blank=True)
    high_low_price = models.CharField(max_length=255, null=True, blank=True)
    week_high_low = models.CharField(max_length=255, null=True, blank=True)
    open_price = models.CharField(max_length=255, null=True, blank=True)
    close_price = models.CharField(max_length=255, null=True, blank=True)
    table_listed_shares = models.CharField(max_length=255, null=True, blank=True)
    total_paid_up_value = models.CharField(max_length=255, null=True, blank=True)
    market_capitalization = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name