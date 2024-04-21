from django.core.management.base import BaseCommand
from app1.models import GovernmentData

class Command(BaseCommand):
    help = 'Populate the government database with predefined Aadhar numbers'

    def aadhar_number_exists_in_database(self, aadhar_number):
        return GovernmentData.objects.filter(aadhar_number=aadhar_number).exists()

    def get_age_from_database(self, aadhar_number):
        government_data = GovernmentData.objects.get(aadhar_number=aadhar_number)
        return government_data.age if government_data else None

    def send_otp_to_mobile_number(self, aadhar_number):
        pass

    def handle(self, *args, **kwargs):
        # Predefined Aadhar numbers, mobile numbers, and ages
        aadhar_numbers = [123456789101, 987654321098, 555555555555, 111111111111, 222222222222, 888888888888]
        mobile_numbers = [9770289451, 1234567890, 8871842515, 7024682316, 9953037903, 8639335723]
        ages = [16, 19, 22, 25, 21, 10]

        # Populate the database with predefined data
        for aadhar, mobile, age in zip(aadhar_numbers, mobile_numbers, ages):
            GovernmentData.objects.create(aadhar_number=aadhar, mobile_number=mobile, age=age)

        self.stdout.write(self.style.SUCCESS('Government database populated successfully'))
