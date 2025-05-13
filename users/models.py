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

        if str(string).__contains__('E+'):
            num = int(float(string))
            return str(num)
        return str(string).strip().title()

    @staticmethod
    def get_datetime_(date_string):
        if type(date_string) == str:
            # Remove ordinal suffixes: 1st, 2nd, 3rd, 4th, etc.
            date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', str(date_string).strip())

            # Try different possible formats
            for fmt in ("%B-%d-%Y", "%B %d, %Y", "%d-%b-%Y", "%m/%d/%y", "%m/%d/%Y"):
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
        return None

    def row_to_correct_dict(self, row):
        return {'id': row['Employee ID'], 'first_name': self.cleanUp(row['First Name']), 'middle_name': self.cleanUp(row['Middle Name']),
                'last_name': self.cleanUp(row['Last Name']), 'start_date': self.get_datetime_(row['Start Date']),
                'birth_date': self.get_datetime_(row['Birthdate']), 'gender': self.cleanUp(row['Gender']),
                'marital_status': self.cleanUp(row['Marital Status']), 'permanent_address': self.cleanUp(row['Permanent Address']),
                'temporary_address': self.cleanUp(row['Temporary Address']), 'contact_no': self.cleanUp(row['Contact Number']),
                'alternate_no': self.cleanUp(row['Alternate Number']), 'emergency_contact': self.cleanUp(row['Emergency Contact #']),
                'alternate_ec': self.cleanUp(row['Alternate Emergency Number']), 'ec_person': self.cleanUp(row['Name of Emergency Contact Person']),
                'email': self.cleanUp(row['Email Address']), 'mothers_maiden_name': self.cleanUp(row['Mother\'s Maiden Name']),
                'father_name': self.cleanUp(row['Father\'s Name']), 'sss_no': self.cleanUp(row['SSS Number']),
                'philhealth_no': self.cleanUp(row['Philhealth Number']), 'hdmf_no': self.cleanUp(row['HDMF Number']),
                'status': self.cleanUp(row['STATUS']), 'tin_id_no': self.cleanUp(row['TIN ID Number']),
                'ended_date': self.get_datetime_(row['DATE'])}

    def record(self, row):
        employee = self.row_to_correct_dict(row)
        if employee['start_date']:
            try:
                return self.get(id=employee['id'])
            except ObjectDoesNotExist:
                return self.create(**employee)
        return None

    def sync_bbc_spreadsheet(self):
        # Construct the CSV export URL
        csv_url = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=csv&gid={self.gid}"

        # Load into pandas DataFrame
        df = pd.read_csv(csv_url, dtype=str)
        for _, row in df.iterrows():
            self.record(row)

class Employees(models.Model):
    id = models.CharField(primary_key=True)
    start_date = models.DateField()
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=50, null=True)
    marital_status = models.CharField(max_length=100, null=True)
    permanent_address = models.TextField(null=True)
    temporary_address = models.TextField(null=True)
    contact_no = models.CharField(max_length=50, null=True)
    alternate_no = models.CharField(max_length=50, null=True)
    emergency_contact = models.CharField(max_length=50, null=True)
    alternate_ec = models.CharField(max_length=50, null=True)
    ec_person = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    mothers_maiden_name = models.CharField(max_length=255, null=True)
    father_name = models.CharField(max_length=255, null=True)
    sss_no = models.CharField(max_length=100, null=True)
    philhealth_no = models.CharField(max_length=100, null=True)
    hdmf_no = models.CharField(max_length=100, null=True)
    tin_id_no = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    ended_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    objects = EmployeesManager()

class JobInformation(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    line_of_business = models.CharField(max_length=50, null=True)
    classification = models.CharField(max_length=50, null=True)
    campaign = models.CharField(max_length=200, null=True)
    work_setup = models.CharField(max_length=100, null=True)
    site = models.CharField(max_length=50, null=True)
    emr = models.CharField(max_length=100, null=True)
    phone_system = models.CharField(max_length=50, null=True)
    client_name = models.CharField(max_length=200, null=True)
    work_days = models.CharField(max_length=50, null=True)
    rest_days = models.CharField(max_length=50, null=True)
    schedule_est = models.CharField(max_length=50, null=True)
    lunch_break_est = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
