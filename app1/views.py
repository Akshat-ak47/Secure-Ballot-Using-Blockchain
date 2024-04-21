from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .management.commands.populate_gov_db import Command
from app1.models import GovernmentData, PrimaryVoterDatabase, SecondaryVoterDatabase
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import check_password
from django.core.serializers import serialize
from django import forms
from django.contrib import messages
from .models import Official, Vote, Hash, Certificate, Event, Team
from .serializers import EventSerializer, TeamSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .forms import EventForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_POST
from django.conf import settings

import hashlib
import logging

# Create your views here.
logger = logging.getLogger(__name__)

@login_required
@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event = form.save()

            # Process team data
            num_teams = int(request.POST.get('num_teams'))
            for i in range(num_teams):
                team_name = request.POST.get('parties[' + str(i+1) + '][name]')
                team_image = request.FILES.get('parties[' + str(i+1) + '][image]')
                team = Team(name=team_name, event=event, image=team_image)
                team.save()

            return JsonResponse({'message': 'Event created successfully', 'event_id': event.event_id}, status=201)
        else:
            print(form.errors)

            return JsonResponse({'error': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['GET'])
def get_events(request):
    events = Event.objects.all().prefetch_related('teams')
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def event_details(request, event_name):
    try:
        event = Event.objects.get(event_name=event_name)
        serializer = EventSerializer(event)
        return JsonResponse(serializer.data)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)


@login_required
def home_view(request):
    upcoming_events = list(Event.objects.values_list('event_name', flat=True))
    request.session['upcoming_events'] = upcoming_events
    return render(request, 'home.html')

@login_required
def homes_view(request):
    upcoming_events = list(Event.objects.values_list('event_name', flat=True))
    request.session['upcoming_events'] = upcoming_events
    return render(request, 'homes.html')

def fetch_upcoming_events(request):
    upcoming_events = Event.objects.values_list('event_name', flat=True)
    request.session['upcoming_events'] = upcoming_events
    print("Upcoming Events:", upcoming_events)
    return render(request, 'home.html', {'upcoming_events': upcoming_events})

def fetch_event_details(request):
    event_name = request.GET.get('event_name')
    event = Event.objects.filter(event_name=event_name).first()
    if event:
        event_details = {
            'event_id': event.id,
            'event_purpose': event.purpose
        }
        return JsonResponse(event_details)
    else:
        return JsonResponse({'error': 'Event not found'}, status=404)

@login_required
def download_cert(request):
    return render(request, 'download_cert.html')

@login_required
def official_dashboard(request):
    official_username = request.session.get('official_username')

    if official_username:
        try:
            official = Official.objects.get(Username=official_username)
            government_data = GovernmentData.objects.get(aadhar_number=official.Aadhar_Number)
            mobile_number = government_data.mobile_number

            context = {
                'username': official.Username,
                'full_name': official.FULLName,
                'email': official.Email,
                'phone_number': mobile_number,
                'age': government_data.age
            }
            upcoming_events = list(Event.objects.values_list('event_name', flat=True))
            events = Event.objects.values('event_name', 'event_id', 'event_purpose')
            request.session['upcoming_events'] = upcoming_events
            request.session['events'] = list(events)

            teams_data = {}
            for event in events:
                teams = Team.objects.filter(event_id=event['event_id'])
                team_data = serialize('json', teams)
                teams_data[event['event_id']] = team_data
            request.session['teams'] = teams_data
            print(team_data)
            return render(request, 'official_dashboard.html', context)
        except Official.DoesNotExist:
            return render(request, 'official_login.html', {'error_message': 'Official details not found'})
        except GovernmentData.DoesNotExist:
            return render(request, 'official_login.html', {'error_message': 'Government data not found'})
    else:
        return redirect('official_login')

def voter_login(request):
    return render(request, 'voter_login.html')

def verify_otp1_view(request):
    return render(request, 'verify_otp1.html')

def verify_otp2_view(request):
    return render(request, 'verify_otp2.html')

def verify_otp3_view(request):
    return render(request, 'verify_otp3.html')

def official_login(request):
    return render(request, 'official_login.html')

def index_view(request):
    return render(request, 'index.html')

def whoru(request):
    return render(request, 'whoru.html')

def face_capture(request):
    return render(request, 'face_capture.html')

def logout_view(request):
    logout(request)
    return redirect('')

from twilio.rest import Client
def generate_otp():
    length = 6
    digits = "0123456789"
    otp = ""
    for _ in range(length):
        otp += random.choice(digits)
    return otp

def send_otp(request):
    otp = generate_otp()

    account_sid = '<Your_Accout_SID>'
    auth_token = '<Your_AUth_Token>'
    twilio_phone_number = '<Your_Twilio_number>'
    recipient_phone_number = '<Recipient_Number>'

    twilio_client = Client(account_sid, auth_token)

    message_body = f'Your OTP is: {otp}'
    twilio_client.messages.create(
        to=recipient_phone_number,
        from_=twilio_phone_number,
        body=message_body
    )
    request.session['otp'] = otp
    return JsonResponse({'success': True})

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        sent_otp = request.session.get('otp')
        if entered_otp == sent_otp:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        aadhar_number = request.POST.get('aadhar_number')
        password = request.POST.get('password')

        try:
            if username:
                official = Official.objects.get(Username=username, Aadhar_Number=aadhar_number)
                if official and check_password(password, official.Password):
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        request.session['official_username'] = official.Username
                        request.session.set_expiry(3600)  # 1 hour
                        return redirect('verify-otp3')
                    else:
                        error_message = 'Invalid username or password'
                        return render(request, 'official_login.html', {'error_message': error_message})
        except Official.DoesNotExist:
            pass

        # If not an official, check if it's a primary voter
        try:
            if aadhar_number:
                primary_voter = PrimaryVoterDatabase.objects.get(aadhar_number=aadhar_number)
                hashed_password = primary_voter.primary_pass
                user = authenticate_voter('primary', aadhar_number, password)
                if user:
                    login(request, user)
                    request.session['unique_address'] = primary_voter.unique_address
                    upcoming_events = list(Event.objects.values_list('event_name', flat=True))
                    request.session['upcoming_events'] = upcoming_events
                    return redirect('verify-otp1')

        except PrimaryVoterDatabase.DoesNotExist:
            pass

        # If not a primary voter, check if it's a secondary voter
        try:
            if aadhar_number:
                secondary_voter = SecondaryVoterDatabase.objects.get(aadhar_number=aadhar_number)
                hashed_password = secondary_voter.secondary_pass
                user = authenticate_voter('secondary', aadhar_number, password)
                if user:
                    login(request, user)
                    request.session['unique_address'] = secondary_voter.unique_address
                    return redirect('verify-otp2')
        except SecondaryVoterDatabase.DoesNotExist:
            pass

        # If none of the above conditions are met, return an error message
        error_message = 'User does not exist or Incorrect password'
        return render(request, 'voter_login.html', {'error_message': error_message})

    # If the request method is not POST, render the voter_login.html template
    return render(request, 'voter_login.html')

def authenticate_voter(voter_type, aadhar_number, password):
    if voter_type == 'primary':
        try:
            voter = PrimaryVoterDatabase.objects.get(aadhar_number=aadhar_number)
        except PrimaryVoterDatabase.DoesNotExist:
            return None
    elif voter_type == 'secondary':
        try:
            voter = SecondaryVoterDatabase.objects.get(aadhar_number=aadhar_number)
        except SecondaryVoterDatabase.DoesNotExist:
            return None

    if check_password(password, voter.primary_pass if voter_type == 'primary' else voter.secondary_pass):
        return voter.user
    else:
        return None

def validate_login(request, aadhar_number, password):
    try:
        voter = VoterData.objects.get(aadhar_number=aadhar_number, primary_password=password)
        return JsonResponse({'success': True, 'passwordType': 'primary'})
    except VoterData.DoesNotExist:
        try:
            voter = VoterData.objects.get(aadhar_number=aadhar_number, secondary_password=password)
            return JsonResponse({'success': True, 'passwordType': 'secondary'})
        except VoterData.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid Aadhar number or password'})

def home_view(request):
    try:
        primary_voter = PrimaryVoterDatabase.objects.get(user=request.user)
        government_data = GovernmentData.objects.get(aadhar_number=primary_voter.aadhar_number)
        profile_data = {
            'unique_address': primary_voter.unique_address,
            'aadhar_number': primary_voter.aadhar_number,
            'age': government_data.age,
            'mobile_number': primary_voter.mobile_number,
        }
        upcoming_events = list(Event.objects.values_list('event_name', flat=True))
        events = Event.objects.values('event_name', 'event_id', 'event_purpose')
        request.session['upcoming_events'] = upcoming_events
        request.session['events'] = list(events)
        request.session['aadhar_number'] = primary_voter.aadhar_number
        request.session['username'] = primary_voter.unique_address

        teams_data = {}
        for event in events:
            teams = Team.objects.filter(event_id=event['event_id'])
            team_data = serialize('json', teams)
            teams_data[event['event_id']] = team_data
        request.session['teams'] = teams_data
        print(team_data)
    except PrimaryVoterDatabase.DoesNotExist:
        profile_data = None
    except GovernmentData.DoesNotExist:
        profile_data = None
        
    return render(request, 'home.html', {'profile_data': profile_data})

def homes_view(request):
    try:
        primary_voter = PrimaryVoterDatabase.objects.get(user=request.user)
        government_data = GovernmentData.objects.get(aadhar_number=primary_voter.aadhar_number)
        profile_data = {
            'unique_address': primary_voter.unique_address,
            'aadhar_number': primary_voter.aadhar_number,
            'age': government_data.age,
            'mobile_number': primary_voter.mobile_number,
        }
        upcoming_events = list(Event.objects.values_list('event_name', flat=True))
        events = Event.objects.values('event_name', 'event_id', 'event_purpose')
        request.session['upcoming_events'] = upcoming_events
        request.session['events'] = list(events)
        request.session['aadhar_number'] = primary_voter.aadhar_number
        request.session['username'] = primary_voter.unique_address

        teams_data = {}
        for event in events:
            teams = Team.objects.filter(event_id=event['event_id'])
            team_data = serialize('json', teams)
            teams_data[event['event_id']] = team_data
        request.session['teams'] = teams_data
        print(team_data)
    except PrimaryVoterDatabase.DoesNotExist:
        profile_data = None
    except GovernmentData.DoesNotExist:
        profile_data = None
        
    return render(request, 'homes.html', {'profile_data': profile_data})

def events_list(request):
    events = request.session.get('events', [])
    return JsonResponse(events, safe=False)

def event_list(request):
    events = Event.objects.all()
    event_data = []
    for event in events:
        event_data.append({
            'event_id': event.event_id,
            'event_name': event.event_name,
            'num_teams': event.num_teams,
            'event_purpose': event.event_purpose,
            'created_at': event.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse(event_data, safe=False)

def logout_view(request):
    logout(request)
    return redirect('voter_login')

def signup_view(request):
    if request.method == 'POST':
        aadhar_number = request.POST.get('aadhar_number')
        primary_password = request.POST.get('primary_password')
        secondary_password = request.POST.get('secondary_password')
        try:
            gov_data = GovernmentData.objects.get(aadhar_number=aadhar_number)
        except GovernmentData.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Aadhar number not found in database'})

        if gov_data.age < 18:
            return JsonResponse({'success': False, 'message': 'You must be 18 years or older to sign up.'})
        
        mobile_number = gov_data.mobile_number
        try:
            user = User.objects.create_user(username=aadhar_number, password=primary_password)
            unique_address = get_random_string(length=32)

            primary_voter = PrimaryVoterDatabase.objects.create(
                user=user,
                unique_address=unique_address,
                aadhar_number=aadhar_number,
                mobile_number=mobile_number,
                primary_pass=make_password(primary_password)
            )

            secondary_voter = SecondaryVoterDatabase.objects.create(
                user=user,
                unique_address=unique_address,
                aadhar_number=aadhar_number,
                mobile_number=mobile_number,
                secondary_pass=make_password(secondary_password)
            )

            return redirect('voter_login')

        except Exception as e:
            print("Error creating or saving VoterDatabase object:", e)
            return JsonResponse({'success': False, 'message': 'Error creating or saving voter account'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})

def official_signup_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        aadhar_number = request.POST.get('aadhar_number')
        password = request.POST.get('password')
        try:
            gov_data = GovernmentData.objects.get(aadhar_number=aadhar_number)
        except GovernmentData.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Aadhar number not found in database'})

        if gov_data.age < 18:
            return JsonResponse({'success': False, 'message': 'You must be 18 years or older to sign up.'})

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            official = Official(
                FULLName=full_name,
                Username=username,
                Email=email,
                Aadhar_Number=aadhar_number,
                Password=make_password(password)
            )
            official.save()
            
            return redirect('official_login')

        except Exception as e:
            print("Error creating or saving Official object:", e)
            return JsonResponse({'success': False, 'message': 'Error creating or saving official account'})

    return render(request, 'official_login')

def validate_aadhar(request, aadhar_number):
    if GovernmentData.objects.filter(aadhar_number=aadhar_number).exists():
        return JsonResponse({'success': True, 'message': 'Aadhar number is valid.'})
    else:
        return JsonResponse({'success': False, 'message': 'Aadhar number not found in database.'})


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

def get_events(request):
    events = Event.objects.all().prefetch_related('parties')
    events_data = []
    for event in events:
        event_data = {
            'event_name': event.event_name,
            'event_purpose': event.event_purpose,
            'parties': [party.name for party in event.parties.all()]
        }
        events_data.append(event_data)
    return JsonResponse(events_data, safe=False)

@csrf_exempt
def save_vote(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        username = request.session.get('username')
        aadhar_number = request.session.get('aadhar_number')
        print(team_name, username, aadhar_number)

        if username is None or aadhar_number is None:
            return JsonResponse({'error': 'User information missing. Unable to save vote.'}, status=400)

        voter_input = username + team_name + aadhar_number
        voter_hash = hashlib.sha256(voter_input.encode()).hexdigest()
        
        last_vote = Vote.objects.last()
        previous_hash = last_vote.voter_hash if last_vote else '0'

        vote = Vote.objects.create(
            team_name=team_name,
            voter_hash=voter_hash,
            previous_hash=previous_hash,
            username=username,
            aadhar_number=aadhar_number
        )
        vote.save()
        hashs = Hash.objects.create(
        voter_hash=voter_hash,
        previous_hash=previous_hash
        )
        hashs.save()
        print("Saved")
        return redirect('download_certificate')
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def send_notification(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        aadhar_number = request.session.get('aadhar_number')

        notification_message = request.POST.get('message')

        print(f"Notification sent: {notification_message}")
        print(f"User Aadhar number: {aadhar_number}")
        
        return JsonResponse({'message': 'Notification sent successfully.'})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)



import cv2
import random
import string
import os

def generate_verification_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def modify_certificate(input_image_path, user_aadhar_number):
    certificate_img = cv2.imread(input_image_path)
    
    if certificate_img is None:
        return None

    user_aadhar_number = ' '.join([user_aadhar_number[i:i+4] for i in range(0, len(user_aadhar_number), 4)])

    # Defining text parameters for Aadhar number
    text = f'{user_aadhar_number}'
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.8
    font_thickness = 2
    font_color = (255, 255, 255)  # White color
    shadow_color = (0, 0, 0)  # Black color for shadow
    shadow_offset = 2

    # Define text parameters for verification code at the bottom
    verification_code = generate_verification_code()
    text_bottom = f'Verification Code: {verification_code}'
    bottom_font_scale = 1
    bottom_font_thickness = 1
    bottom_font_color = (255, 255, 255)  # White color

    # Get text size for Aadhar number
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_width, text_height = text_size

    # Calculate text position for Aadhar number
    text_x = int((certificate_img.shape[1] - text_width) / 2)
    text_y = int((certificate_img.shape[0] + text_height) / 2)
    text_position = (text_x, text_y)

    # Get text size for bottom text
    bottom_text_size = cv2.getTextSize(text_bottom, font, bottom_font_scale, bottom_font_thickness)[0]
    bottom_text_width, bottom_text_height = bottom_text_size

    # Calculate text position for bottom text
    bottom_text_x = int((certificate_img.shape[1] - bottom_text_width) / 2)
    bottom_text_y = certificate_img.shape[0] - 40

    cv2.putText(certificate_img, text, (text_x + shadow_offset, text_y + shadow_offset), font, font_scale,
                shadow_color, font_thickness)

    # Add Aadhar number
    cv2.putText(certificate_img, text, text_position, font, font_scale, font_color, font_thickness)

    # Add verification code at the bottom
    cv2.putText(certificate_img, text_bottom, (bottom_text_x, bottom_text_y), font, bottom_font_scale,
                bottom_font_color, bottom_font_thickness)

    # Encode the modified image as JPEG
    _, img_encoded = cv2.imencode('.jpg', certificate_img)
    
    certificate = Certificate(aadhar_number=user_aadhar_number, verification_code=verification_code)
    certificate.save()
    return img_encoded.tobytes()

def download_certificate(request):
    BASE_DIR = settings.BASE_DIR
    # Path to the input certificate image
    input_image_path = os.path.join(BASE_DIR, 'templates', 'static', 'assets', 'img', 'vote.png')

    # User's Aadhar number
    user_aadhar_number = request.session.get('aadhar_number')

    # Generate the modified certificate
    modified_certificate_bytes = modify_certificate(input_image_path, user_aadhar_number)

    if modified_certificate_bytes is not None:
        # Serve the modified certificate for download
        response = HttpResponse(modified_certificate_bytes, content_type="image/jpeg")
        response['Content-Disposition'] = 'attachment; filename="secBallot_certificate.jpg"'
        return response
    else:
        return HttpResponse("Error: Unable to modify the certificate", status=500)


def error_404(request, exception):
    return render(request, '404.html', status=404)

def verify_vote(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        team_names = request.POST.getlist('team_names[]')
        
        print("Event ID:", event_id)
        print("Team Names:", team_names)
        
        team_counts = {}
        for team_name in team_names:
            count = Vote.objects.filter(team_name=team_name).count()
            team_counts[team_name] = count
        
        request.session['team_counts'] = team_counts
        return render(request, 'verify_vote.html', {'team_counts': team_counts})
    elif request.method == 'GET':
        team_counts = request.session.get('team_counts', {})
        
        return render(request, 'verify_vote.html', {'team_counts': team_counts})
    else:
        return render(request, 'verify_vote.html')


def verify_votes(request):
    votes_tampered = False
    votes = Vote.objects.all()

    voter_hashes = Hash.objects.values_list('previous_hash', flat=True)
    print("Voter Hashes from Database:", voter_hashes)

    for vote in votes:
        voter_input = f"{vote.username}{vote.team_name}{vote.aadhar_number}"
        voter_hash = hashlib.sha256(voter_input.encode()).hexdigest()

        print("Vote:", vote.id, "Calculated Hash:", voter_hash)

        if voter_hash not in voter_hashes:
            votes_tampered = True
            break
    return JsonResponse({'tampered': votes_tampered})


@csrf_exempt
def render_verify_certificate(request):
    if request.method == "GET":
        return render(request, 'verify_certificate.html')
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code', '')
        print("Received verification code:", verification_code)

        try:
            certificate = Certificate.objects.get(verification_code=verification_code)
            print("Certificate found:", certificate)
            return JsonResponse({'exists': True, 'aadhar_number': certificate.aadhar_number})
        except Certificate.DoesNotExist:
            print("Certificate not found")
            return JsonResponse({'exists': False})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
