import re
import pandas as pd
from datetime import datetime
from django.db import models
from django.core.exceptions import ObjectDoesNotExist



class EmployeesManager(models.Manager):
    sheet_id = "1CvTfC-cuYmVnvFoevBvrsAwZwgWP-m--foohtKYMMuY"
    gid = "0"

    @staticmethod
    def cleanUp(string):
        if type(string) == float:
            return None
        return str(string).lower()

    @staticmethod
    def get_datetime_(date_string):
        if type(date_string) == str:
            if len(str(date_string).split('/')) == 3:
                return datetime.strptime(date_string, '%m/%d/%Y')

            # Remove the ordinal suffix using regex
            cleaned_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_string)
            return datetime.strptime(cleaned_str, "%B-%d-%Y")
        return None

    def row_to_correct_dict(self, row):
        return {'id': row['Employee ID'], 'first_name': self.cleanUp(row['First Name']), 'middle_name': self.cleanUp(row['Middle Name']),
                'last_name': self.cleanUp(row['Last Name']), 'start_date': self.get_datetime_(row['Start Date']),
                'birth_date': self.get_datetime_(row['Birthdate']), 'gender': self.cleanUp(row['Gender']),
                'marital_status': self.cleanUp(row['Marital Status']), 'permanent_address': self.cleanUp(row['Permanent Address']),
                'temporary_address': self.cleanUp(row['Temporary Address']), 'contact_no': row['Contact Number'],
                'alternate_no': row['Alternate Number'], 'emergency_contact': row['Emergency Contact #'],
                'alternate_ec': row['Alternate Emergency Number'], 'ec_person': row['Name of Emergency Contact Person'],
                'email': row['Email Address'], 'mothers_maiden_name': row['Mother\'s Maiden Name'],
                'father_name': row['Father\'s Name'], 'sss_no': row['SSS Number'],
                'philhealth_no': row['Philhealth Number'], 'hdmf_no': row['HDMF Number'], 'status': row['STATUS'],
                'tin_id_no': row['TIN ID Number'], 'ended_date': self.get_datetime_(row['DATE'])}

    def record(self, row):
        employee = self.row_to_correct_dict(row)

        try:
            return self.get(id=employee['id'])
        except ObjectDoesNotExist:
            return self.create(**employee)

    def sync_bbc_spreadsheet(self):
        # Construct the CSV export URL
        csv_url = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=csv&gid={self.gid}"

        # Load into pandas DataFrame
        df = pd.read_csv(csv_url)
        for _, row in df.iterrows():
            self.record(row)

class Employees(models.Model):
    id = models.CharField(primary_key=True)
    start_date = models.DateField()
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=100)
    permanent_address = models.TextField()
    temporary_address = models.TextField()
    contact_no = models.CharField(max_length=50, null=True)
    alternate_no = models.CharField(max_length=50, null=True)
    emergency_contact = models.CharField(max_length=50, null=True)
    alternate_ec = models.CharField(max_length=50, null=True)
    ec_person = models.CharField(max_length=200, null=True)
    email = models.EmailField()
    mothers_maiden_name = models.CharField(max_length=255, null=True)
    father_name = models.CharField(max_length=255, null=True)
    sss_no = models.CharField(max_length=50, null=True)
    philhealth_no = models.CharField(max_length=50, null=True)
    hdmf_no = models.CharField(max_length=50, null=True)
    tin_id_no = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50)
    ended_date = models.DateField(null=True)
    objects = EmployeesManager()
