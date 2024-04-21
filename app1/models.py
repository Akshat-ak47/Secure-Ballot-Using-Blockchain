from django.db import models
from django.contrib.auth.models import User


class Vote(models.Model):
    team_name = models.CharField(max_length=100)
    voter_hash = models.CharField(max_length=64)
    previous_hash = models.CharField(max_length=64)
    username = models.CharField(max_length=100)
    aadhar_number = models.CharField(max_length=12)
    
class Hash(models.Model):
    voter_hash = models.CharField(max_length=64)
    previous_hash = models.CharField(max_length=64)

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100)
    num_teams = models.IntegerField()
    event_purpose = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    dummy_field = models.CharField(max_length=1, blank=True, null=True)


class Team(models.Model):
    event = models.ForeignKey(Event, related_name='teams', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_images/')

    def __str__(self):
        return f"Team: {self.name} (Event: {self.event.event_name})"

class GovernmentData(models.Model):
    aadhar_number = models.BigIntegerField(unique=True)
    mobile_number = models.BigIntegerField(unique=True)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"Aadhar: {self.aadhar_number}, Mobile: {self.mobile_number}, Age: {self.age}"

class YourModel(models.Model):
    id = models.BigAutoField(primary_key=True)  # Explicitly define primary key

    # Your other fields here

class PrimaryVoterDatabase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_address = models.CharField(max_length=255)
    aadhar_number = models.CharField(max_length=12, unique=True)
    mobile_number = models.CharField(max_length=10)
    primary_pass = models.CharField(max_length=128)

class SecondaryVoterDatabase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_address = models.CharField(max_length=255)
    aadhar_number = models.CharField(max_length=12, unique=True)
    mobile_number = models.CharField(max_length=10)
    secondary_pass = models.CharField(max_length=128)

    def __str__(self):
        return f"Voter Data: Aadhar - {self.aadhar_number}"

class Official(models.Model):
    FULLName = models.CharField(max_length=100)
    Username = models.CharField(max_length=50, unique=True)
    Email = models.EmailField(unique=True)
    Aadhar_Number = models.CharField(max_length=12, unique=True)
    Password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.Username


class Certificate(models.Model):
    aadhar_number = models.CharField(max_length=16)
    verification_code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"Aadhar Number: {self.aadhar_number}, Verification Code: {self.verification_code}"
