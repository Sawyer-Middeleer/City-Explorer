from django.db import models
from django import forms
from django.conf import settings
from django.utils import timezone
from bs4 import BeautifulSoup
import urllib
import re
import csv
import io

# user input
class PropAddress(models.Model):
    pin = models.CharField(max_length=14)
    tax_code = models.CharField(max_length=6)
    # tax_code needs to come from scraping the assessor's website
    def __str__(self):
        return self.pin

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])

    def get_tax_code(self):
        """Scrapes the Cook County Assessor's website to grab the PIN's tax code"""
        with urllib.request.urlopen('http://www.cookcountyassessor.com/Property.aspx?mode=details&pin='+self.pin) as url:
            html = url.read()
        bsObj = BeautifulSoup(html)
        tax_code_obj = bsObj.find(id="ctl00_phArticle_ctlPropertyDetails_lblPropInfoTaxcode")
        self.tax_code = tax_code_obj.get_text()
        self.save()

# from tax_rates csv
class TaxCode(models.Model):
    tax_year = models.IntegerField(default=2017)
    tax_code = models.IntegerField(default=12345)
    agency = models.IntegerField(default=10010000)
    agency_name = models.CharField(default="COUNTY OF COOK", max_length=50)
    agency_rate = models.DecimalField(default=0, decimal_places=3, max_digits=6)
    tax_code_rate = models.DecimalField(default=0, decimal_places=3, max_digits=6)
    assessment_district = models.CharField(default="Barrington", max_length=50)
    taxing_body_count = models.IntegerField(default=0)
    equalization_factor = models.DecimalField(default=2.0, decimal_places=3, max_digits=6)
    user_address = models.ForeignKey(PropAddress, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.tax_code)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])

    def read_tax_rates_data(self):
        with open(r'C:\Users\midde\OneDrive\Documents\GitHub\IL-Gov-Counter\il_gov_counter\cctaxes\static\cctaxes\oak_park_rates.csv', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'Tax Year':
                    _, created = TaxCode.objects.get_or_create(
                        tax_year=row[0],
                        tax_code=row[1],
                        agency=row[2],
                        agency_name=row[3],
                        agency_rate=row[4],
                        tax_code_rate=row[5],
                        assessment_district=row[6],
                        taxing_body_count=row[7],
                        equalization_factor=row[8]
                    )
                # creates a tuple of the new object or
                # current object and a boolean of if it was created