from django.core.paginator import Paginator
from django.db.models import F, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, ChatbotClientSerializer, ClientSerializer, ClientPhoneSerializer, ClientSymptomQuestionAnswerSerializer
from django.contrib.auth.models import User, Group
from callcenter.models import TxRegime, InvestigationType, ClientRefRegLocation, InvestigationResult, SiteLocation, ChatbotClient, Client, ClientPhone, ClientSymptomQuestionAnswer, Township, StateRegion, Channel
from django.views.generic.base import TemplateView
from rest_framework import generics
#from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from callcenter.forms import SymptomByCallForm, StageFilterForm, TBTreatmentForm, TBConfirmationForm, InvestigationForm, ReachInfoForm, AdditionalPhoneForm ,ReferLocationForm, SearchForm, FirstContactForm, TBReferralForm, ActiveSocialPlatformsForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests, json
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from datetime import datetime


@login_required
# def index(request):
#     form = SearchForm(request.GET)
#     client_phones = ClientPhone.objects.filter(phone_type__iexact="1").order_by('client__stage','modified_datetime')
#     if form.is_valid():
#         query = form.cleaned_data['query']
#         client_phones = ClientPhone.objects.filter(phone_type__iexact="1", phone_number__icontains=query).order_by('client__stage','modified_datetime')
#     return render(request, 'callcenter/index.html', {'client_phones': client_phones, 'form': form})
def index(request):
    stage_filter_form = StageFilterForm(request.GET)
    query = request.GET.get('query', '')

    filter_conditions = Q()

    if stage_filter_form.is_valid():
        stage = stage_filter_form.cleaned_data.get('stage')
        if stage:
            filter_conditions &= Q(client__stage=stage)

    if query:
        filter_conditions &= Q(phone_number__icontains=query)

    client_phones = ClientPhone.objects.select_related('client').filter(filter_conditions).order_by('created_datetime','phone_number')

    # Pagination
    paginator = Paginator(client_phones, 10)  # Show 10 clients per page
    page = request.GET.get('page')
    clients_page = paginator.get_page(page)

    context = {
        'client_phones': clients_page,
        'stage_filter_form': stage_filter_form,
    }

    return render(request, 'callcenter/index.html', context)









# def index(request):
#     if request.user.is_authenticated:
#         context = {
#             'abc': 'abc',
#         }
#         return render(request,'callcenter/index.html',context)
#     else:
#         return redirect(reverse('login') + '?next=' + request.path)

def test(request):
    context = {
        'a':'a'
    }
    return render(request,'callcenter/testPage.html',context)

def testone(request):
    return render(request,'callcenter/testone.html',{})

def create_client(request):
    return render(request,'callcenter/createClient.html',{})

def test_co_pilot(request):
    return render(request,'callcenter/testcopilot.html',{'pageTitle':'Login'})

def new_tb_referral(request):
    return render(request,'callcenter/new-tb-referral.html',{'pageTitle':'New TB Referral'})

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatbotClientViewSet(viewsets.ModelViewSet):
    queryset = ChatbotClient.objects.all()
    serializer_class = ChatbotClientSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClientPhoneViewSet(viewsets.ModelViewSet):
    queryset = ClientPhone.objects.all()
    serializer_class = ClientPhoneSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClientSymptomQuestionAnswerViewSet(viewsets.ModelViewSet):
    queryset = ClientSymptomQuestionAnswer.objects.all()
    serializer_class = ClientSymptomQuestionAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientSymptomQuestionAnswerView(generics.ListCreateAPIView):
    serializer_class = ClientSymptomQuestionAnswerSerializer

    def get_serializer(self, *args, **kwargs):
            if isinstance(kwargs.get("data", {}), list):
                kwargs["many"] = True
            return super(ClientSymptomQuestionAnswerView, self).get_serializer(*args, **kwargs)


# class ProductView(generics.ListCreateAPIView):
#     serializer_class = serializers.ProductSerializer

#     def get_serializer(self, *args, **kwargs):
#         if isinstance(kwargs.get("data", {}), list):
#             kwargs["many"] = True

#     return super(ProductView, self).get_serializer(*args, **kwargs)


# class ClientCreateAPIView(generics.CreateAPIView):
#     """
#     Create a new Client entry with ModelB entry
#     """
#     queryset = Client.objects.all()
#     serializer_class = ClientCreateSerializer
#     permission_classes = [permissions.IsAuthenticated]

class CaseListView(TemplateView):

    template_name = "callcenter/case_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['case_list'] = '' #Article.objects.all()[:5]
        return context

# class LoginView(TemplateView):

#     template_name = "callcenter/login.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['case_list'] = '' #Article.objects.all()[:5]
#         context['title'] = 'Login'
#         return context


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the page the user came from, or to a default URL
            return redirect(request.GET.get('next', '/'))
        else:
            # Return an error message
            return render(request, 'callcenter/login.html', {'error': 'Invalid username or password'})
    else:
        # Render the login form
        return render(request, 'callcenter/login.html')

@login_required
def client_details(request, id):
    client = get_object_or_404(Client, id=id)

    if client:
        tb_referral_client = client.tbreferralclient_set.all()
        client_phones = client.clientphone_set.all()
        client_primary_phone = client_phones.get(phone_type__exact='1')
        client_additional_phone = client_phones.filter(phone_type__exact='2')


        call_attempts = client.callattempt_set.all().order_by('created_datetime')
        stage1_contact_call_attempts = call_attempts.filter(stage__id__exact=2)
        stage2_diagnosis_call_attempts = call_attempts.filter(stage__id__exact=5)
        stage3_register_call_attempts = call_attempts.filter(stage__id__exact=6)

        client_symptoms_questions_answers = client.clientsymptomquestionanswer_set.all().order_by('created_datetime')
        client_chatbot_symptoms_questions_answers = client_symptoms_questions_answers.filter(stage__id__exact=1)
        client_call_symptoms_questions_answers = client_symptoms_questions_answers.filter(stage__id__exact=2)

        client_tb_referral = client.clienttbreferral_set.all()

        client_social_platforms = client.clientsocialplatform_set.all()

        client_ref_reg_locations = client.clientrefreglocation_set.all()
        client_ref_locations = client_ref_reg_locations.filter(action_type__exact='1')
        client_reg_locations = client_ref_reg_locations.filter(action_type__exact='2')

        client_reach_info = client.clientreachinfo_set.all()

        client_investigated_results = client.clientinvestigatedresult_set.all()

        client_tb_confirmation = client.clienttbconfirmation_set.all()

        client_tb_treatment = client.clienttbtreatment_set.all()

    context = {
        'client': client,
        'tb_referral_client': tb_referral_client,
        'client_primary_phone': client_primary_phone,
        'client_additional_phone': client_additional_phone,
        'call_attempts': call_attempts,
        'stage1_contact_call_attempts': stage1_contact_call_attempts,
        'stage2_diagnosis_call_attempts': stage2_diagnosis_call_attempts,
        'stage3_register_call_attempts': stage3_register_call_attempts,
        'client_symptoms_questions_answers': client_symptoms_questions_answers,
        'client_chatbot_symptoms_questions_answers': client_chatbot_symptoms_questions_answers,
        'client_call_symptoms_questions_answers': client_call_symptoms_questions_answers,
        'client_tb_referral': client_tb_referral,
        'client_social_platforms': client_social_platforms,
        'client_ref_reg_locations': client_ref_reg_locations,
        'client_ref_locations': client_ref_locations,
        'client_reg_locations': client_reg_locations,
        'client_reach_info': client_reach_info,
        'client_investigated_results': client_investigated_results,
        'client_tb_confirmation': client_tb_confirmation,
        'client_tb_treatment': client_tb_treatment,
    }
    return render(request,'callcenter/client_detail.html',context)

class ClientNewPhView(TemplateView):

    template_name = "callcenter/client_new_ph.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['case_list'] = '' #Article.objects.all()[:5]
        return context

def client_new_phone(request, pk):
    context={
        'pk':pk
    }
    return render(request,'callcenter/client_new_ph.html',context)

def client_stage1_new_contact(request, pk):
    context={
        'pk':pk
    }
    return render(request,'callcenter/client_stage1_new_contact.html',context)


def client_stage1_additional_contact(request, pk):
    context={
        'pk':pk
    }
    return render(request,'callcenter/client_stage1_additional_contact.html',context)

def client_stage2_new_diagnosis(request, pk):
    context={
        'pk':pk
    }
    return render(request,'callcenter/client_stage2_new_diagnosis.html',context)

def client_stage2_new_investigation(request,pk):
    context={
        'pk':pk
    }
    return render(request,'callcenter/client_stage2_new_investigation.html',context)

def client_stage3_new_tb_register(request,pk):
    context={
        'pk':pk
    }
    return render(request,'callcenter/client_stage3_new_tb_register.html',context)

def client_edit(request,id):
    context = {

        }
    return render(request, 'callcenter/client_edit.html', context)

# @login_required
# def first_contact(request, id):
#     client = get_object_or_404(Client, id=id)
#     client_phone = client.clientphone_set.get(phone_type='1')

#     if request.method == 'POST':
#         form = FirstContactForm(request.POST)
#         if form.is_valid():
#             # Process form data
#             # name = form.cleaned_data['name']
#             # email = form.cleaned_data['email']
#             # message = form.cleaned_data['message']
#             can_contact = form.cleaned_data['can_contact']
#             age_range = form.cleaned_data['age_range']
#             hidden_client_id = form.cleaned_data['hidden_client_id']

#             print(can_contact)
#             print(age_range)
#             print(hidden_client_id)

#             form.save(id=client.id,client_phone=client_phone)
#             # Do something with the form data
#             # ...
#             # Redirect to success page
#             return redirect('client_details', id=id)
#         else:
#             print(form.errors)
#     else:
#         initial_values = {'hidden_client_id': id}
#         form = FirstContactForm(initial=initial_values)

#     return render(request, 'callcenter/client_first_contact.html', {'form': form})

@login_required
def first_contact(request, id):
    try:
        client = get_object_or_404(Client, id=id)
        client_phone = client.clientphone_set.get(phone_type='1')

        if request.method == 'POST':
            print(request.POST)
            form = FirstContactForm(request.POST)
            if form.is_valid():
                can_contact = form.cleaned_data['can_contact']
                age_range = form.cleaned_data['age_range']

                form.save(id=client.id, client_phone=client_phone)

                # Log the form data
                print("Form data:", request.POST)

                return JsonResponse({'success': True, 'user_info': {'can_be_contacted': can_contact, 'age_range': age_range}})
            else:
                # Log the form errors
                print("Form errors:", form.errors)
                return JsonResponse({'success': False, 'error_message': 'Please check the form inputs.'}, status=400)
        else:
            return JsonResponse({'success': False, 'error_message': 'Invalid request method.'}, status=400)
    except Exception as e:
        # Log any exceptions
        print("Exception occurred:", e)
        return JsonResponse({'success': False, 'error_message': 'An error occurred on the server.'}, status=500)

# @login_required
# def symptoms_confirmed_by_call(request, id):
#     client = get_object_or_404(Client, id=id)
#     tb_referral_client = client.tbreferralclient_set.all()


#     if tb_referral_client.first().age_range == "BelowFifteen":
#         if request.method == 'POST':
#             form = SymptomByCallChildForm(request.POST)
#             if form.is_valid():
#                 # Process form data
#                 # name = form.cleaned_data['name']
#                 # email = form.cleaned_data['email']
#                 # message = form.cleaned_data['message']
#                 # can_contact = form.cleaned_data['can_contact']
#                 # age_range = form.cleaned_data['age_range']
#                 # hidden_client_id = form.cleaned_data['hidden_client_id']

#                 print(form.cleaned_data['question1'])
#                 print(form.cleaned_data['question2'])
#                 print(form.cleaned_data['question3'])

#                 form.save(client=client)
#                 # Do something with the form data
#                 # ...
#                 # Redirect to success page
#                 return redirect('client_details', id=id)
#             else:
#                 print(form.errors)
#         else:
#             #initial_values = {'hidden_client_id': id}
#             #form = FirstContactForm(initial=initial_values)
#             form = SymptomByCallChildForm()

#         return render(request, 'callcenter/client_symptoms_by_call_child.html', {'form': form})
#     else:
#         if request.method == 'POST':
#             form = SymptomByCallAdultForm(request.POST)
#             if form.is_valid():
#                 # Process form data
#                 # name = form.cleaned_data['name']
#                 # email = form.cleaned_data['email']
#                 # message = form.cleaned_data['message']
#                 # can_contact = form.cleaned_data['can_contact']
#                 # age_range = form.cleaned_data['age_range']
#                 # hidden_client_id = form.cleaned_data['hidden_client_id']

#                 # print(can_contact)
#                 # print(age_range)
#                 # print(hidden_client_id)

#                 form.save(client=client)
#                 # Do something with the form data
#                 # ...
#                 # Redirect to success page
#                 return redirect('client_details', id=id)
#             else:
#                 print(form.errors)
#         else:
#             #initial_values = {'hidden_client_id': id}
#             #form = FirstContactForm(initial=initial_values)
#             form = SymptomByCallAdultForm()

#         return render(request, 'callcenter/client_symptoms_by_call_adult.html', {'form': form})

@login_required
def symptoms_confirmed_by_call(request, id):
    client = get_object_or_404(Client, id=id)
    tb_referral_client = client.tbreferralclient_set.all()

    age_range = 'a' if tb_referral_client.first().age_range != "BelowFifteen" else 'c'

    if request.method == 'POST':
        form = SymptomByCallForm(request.POST, age_range=age_range)
        if form.is_valid():
            form.save(client=client)
            # return a JSON response with success status and any other details needed
            return JsonResponse({"success": True})
        else:
            # return the form errors
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = SymptomByCallForm(age_range=age_range)

    # if not a POST request, return a default response (you can modify this as needed)
    return JsonResponse({"message": "Invalid request method"})

# @login_required
# def refer_tb_client(request, id):
#     client = get_object_or_404(Client, id=id)

#     if request.method == 'POST':
#         form = TBReferralForm(request.POST)
#         if form.is_valid():
#             # Process form data
#             # name = form.cleaned_data['name']
#             # email = form.cleaned_data['email']
#             # message = form.cleaned_data['message']
#             # can_contact = form.cleaned_data['can_contact']
#             # age_range = form.cleaned_data['age_range']
#             # hidden_client_id = form.cleaned_data['hidden_client_id']

#             # print(can_contact)
#             # print(age_range)
#             # print(hidden_client_id)

#             form.save(client=client)
#             # Do something with the form data
#             # ...
#             # Redirect to success page
#             return redirect('client_details', id=id)
#         else:
#             print(form.errors)
#     else:
#         #initial_values = {'hidden_client_id': id}
#         form = TBReferralForm()

#     return render(request, 'callcenter/client_tb_referral.html', {'form': form})


@login_required
def refer_tb_client(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        form = TBReferralForm(request.POST)
        if form.is_valid():
            form.save(client=client)
            # Return a JSON response instead of a redirect
            return JsonResponse({
                'success': True,
                'is_willing_to_be_referred': form.cleaned_data['willing_to_be_referred'],
                'name': form.cleaned_data['name'],
            })
        else:
            # If form is invalid, return a JSON response with an error message
            return JsonResponse({
                'success': False,
                'error': form.errors,
            })




# @login_required
# def is_active_in_social_platforms(request,id):

#     client = get_object_or_404(Client, id=id)



#     if request.method == 'POST':
#         form = ActiveSocialPlatformsForm(request.POST)
#         if form.is_valid():

#             form.save(client=client)

#             # Redirect to success page
#             return redirect('client_details', id=id)
#         else:
#             print(form.errors)
#     else:
#         #initial_values = {'hidden_client_id': id}
#         form = ActiveSocialPlatformsForm()

#     return render(request, 'callcenter/client_social_platforms.html', {'form': form})


@login_required
def is_active_in_social_platforms(request,id):

    client = get_object_or_404(Client, id=id)



    if request.method == 'POST':
        form = ActiveSocialPlatformsForm(request.POST)
        if form.is_valid():

            form.save(client=client)

            return JsonResponse({
                'success': True,
                'platform1': form.cleaned_data['platform1'],
                'platform2': form.cleaned_data['platform2'],
                'platform3': form.cleaned_data['platform3'],
            })
        else:
            # If form is invalid, return a JSON response with an error message
            return JsonResponse({
                'success': False,
                'error': form.errors,
            })



def send_sms(api_endpoint=None, api_key=None, recipient=None, message=None):
    # url = api_endpoint

    # headers = {
    #     'Content-Type': 'application/json',
    #     'Authorization': 'Bearer ' + api_key
    # }
    # data = {
    #     'to': "+959977287154",
    #     'message': "Hello",
    #     "sender": "NODIS"
    # }


    # payload = json.dumps(data)

    # response = requests.post(url, headers=headers, data=payload)
    # print(response)
    # if response.status_code == 200:
    #     # message sent successfully
    #     return True
    # else:
    #     # handle the error
    #     return False




    # Set up the message details
    message_data = {
        'api_key': 'UyiSZcmawREiHqngViqVgFavGuZKYawFBUYBZrsGqS7HWoxkqV5xtEixXNzvk5sP',
        'phone_number': '+959977287154',  # Replace with the recipient's phone number
        'message': 'Hello from Python!',  # Replace with your message text
        'sender_id': 'CareConnect'  # Replace with your sender ID
    }

    # Send the message using the SMSPOH API
    response = requests.post('https://smspoh.com/api/v1/sms/send', data=message_data)

    # Check the response status code to see if the message was sent successfully
    if response.status_code == 200:
        print('Message sent successfully!')
    else:
        print('Error sending message:', response.text)





# @login_required
# def refer_locations(request, id):

#     client = get_object_or_404(Client, id=id)

#     if request.method == 'POST':
#         form = ReferLocationForm(request.POST)
#         if form.is_valid():
#             # state_region = form.cleaned_data['state_region']
#             township = form.cleaned_data['township'].name_mm
#             # location = Location.objects.create(country=country, city=city)
#             site = form.cleaned_data['site'].site_address_mm
#             clinic = form.cleaned_data['clinic'].clinic_name_mm
#             # channel = form.cleaned_data['channel']
#             # organization = form.cleaned_data['organization']
#             # print(site)

#             form.save(client=client)
#             # if clinic:
#             #     message = f"မင်္ဂလာပါရှင်၊ CareConnect ကပါ၊ ဆေးခန်းလိပ်စာကတော့ {clinic}ဆေးခန်း၊ {site}၊ {township}မြို့နယ်ပါရှင့်။ သာယာတဲ့နေ့လေးတစ်နေ့ဖြစ်ပါစေရှင့်။"
#             # else:
#             #     message = f"မင်္ဂလာပါရှင်၊ CareConnect ကပါ၊ ဆေးခန်းလိပ်စာကတော့ {site}၊ {township}မြို့နယ်ပါရှင့်။ သာယာတဲ့နေ့လေးတစ်နေ့ဖြစ်ပါစေရှင့်။"

#             # send_sms(
#             #     api_endpoint="https://smspoh.com/api/v2/send",
#             #     api_key="UyiSZcmawREiHqngViqVgFavGuZKYawFBUYBZrsGqS7HWoxkqV5xtEixXNzvk5sP",
#             #     recipient=client.clientphone_set.get(client=client,phone_type='1').phone_number,
#             #     message=message
#             # )

#             # Redirect to the success page
#             return redirect('client_details', id=id)
#     else:
#         form = ReferLocationForm()

#     return render(request, 'callcenter/client_referred_location.html', {'form': form})


# @login_required
# def refer_locations(request, id):

#     client = get_object_or_404(Client, id=id)

#     if request.method == 'POST':
#         form = ReferLocationForm(request.POST)
#         if form.is_valid():

#             result = form.save(client=client)
#             id = form.cleaned_data['siteAddress'].value
#             site = get_object_or_404(SiteLocation, id=id)

#             return JsonResponse({
#                 'success': True,
#                 'state_region': site.state_region.name,
#                 'township': site.township.name,
#                 'channel': site.channel.name,
#                 'org': site.organization.name,
#                 'site_address': site.site_address,
#                 'site_address_mm': site.site_address_mm,
#                 'clinic_name': site.clinic_name,
#                 'clinic_name_mm': site.clinic_name_mm,
#                 'referred_date': result.action_date,
#             })

#         else:
#             # If form is invalid, return a JSON response with an error message
#             return JsonResponse({
#                 'success': False,
#                 'error': form.errors,
#             })




@login_required
def refer_locations(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':


        # Manually validate the data
        state_region = request.POST['stateRegion']
        print(state_region)
        township = request.POST['township']
        print(township)
        channel = request.POST['channel']
        print(channel)
        site_address = request.POST['siteAddress']
        print(site_address)
        refer_date = request.POST['referDate']
        print(refer_date)
        site = get_object_or_404(SiteLocation, id=site_address)
        errors = {}
        if not state_region:
            errors['stateRegion'] = 'This field is required.'
        if not township:
            errors['township'] = 'This field is required.'
        if not channel:
            errors['channel'] = 'This field is required.'
        if not site_address:
            errors['siteAddress'] = 'This field is required.'
        if not refer_date:
            errors['referDate'] = 'This field is required.'
        else:
            try:
                refer_date = datetime.strptime(refer_date, '%Y-%m-%d').date()
            except ValueError:
                errors['referDate'] = 'Invalid date format. Expected YYYY-MM-DD.'

        if errors:
            return JsonResponse({'errors': errors}, status=400)

        # If the data is valid, save a new ClientRefLocation
        location = ClientRefRegLocation(
            client=client,
            site_location=site,
            action_date=refer_date,
            action_type='1'
        )
        print(f"{location.client.id},{location.site_location.site_address},{location.action_date},{location.action_type}")
        location.save()
        client.stage_id = 3
        client.save()
        print(f"{site.organization__name}")
        if (location.id):
            return JsonResponse({
                'success': True,
                'message': 'TB Refer Location successfully created.',
                'state_region': site.state_region.name,
                'township': site.township.name,
                'channel': site.channel.name,
                'org': site.organization.name,
                'clinic_name': site.clinic_name,
                'clinic_name_mm': site.clinic_name_mm,
                'provider_name': site.provider_name,
                'provider_name_mm': site.provider_name_mm,
                'site_address': site.site_address,
                'site_address_mm': site.site_address_mm,
                'referred_date': refer_date,
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Something went wrong. Please contact digital health team',
                'error': 'Database error. Please contact digital health team',
            })

        # return JsonResponse({
        #     'success': True,
        #     'message': 'TB Refer Location successfully created.',
        #     'state_region': site.state_region.name,
        #     'township': site.township.name,
        #     'channel': site.channel.name,
        #     'org': site.organization.name,
        #     'clinic_name': site.clinic_name,
        #     'clinic_name_mm': site.clinic_name_mm,
        #     'provider_name': site.provider_name,
        #     'provider_name_mm': site.provider_name_mm,
        #     'site_address': site.site_address,
        #     'site_address_mm': site.site_address_mm,
        #     'referred_date': refer_date,
        # })

    return JsonResponse({'error': 'Invalid request method.'}, status=400)






@login_required
def get_state_regions(request):
    state_regions = StateRegion.objects.annotate(num_sites=Count('sitelocation')).filter(num_sites__gt=0).order_by('name')
    response_data = list(state_regions.values('id', 'name'))
    return JsonResponse(response_data, safe=False)

@login_required
def get_townships(request, state_region_id):
    site_locations = SiteLocation.objects.filter(state_region_id=state_region_id)
    townships = Township.objects.filter(id__in=site_locations.values('township')).order_by('name')
    response_data = list(townships.values('id', 'name'))
    return JsonResponse(response_data, safe=False)

@login_required
@require_http_methods(["GET"])
def get_channels(request, township_id):
    # Get the unique channels associated with the township in SiteLocation model
    channels = Channel.objects.filter(sitelocation__township_id=township_id).distinct().order_by('name')

    # Convert the queryset to a list of dictionaries
    channels_list = list(channels.values('id', 'name'))

    # Return the list as a JSON response
    return JsonResponse(channels_list, safe=False)

@login_required
def get_site_addresses(request, state_region_id, township_id, channel_id):
    site_addresses = SiteLocation.objects.filter(
        state_region_id=state_region_id,
        township_id=township_id,
        channel_id=channel_id
    ).values('id', 'site_address', 'site_address_mm', 'clinic_name', 'clinic_name_mm', 'organization__name')
    site_address_list = list(site_addresses)
    return JsonResponse(site_address_list, safe=False)

@login_required
def load_townships(request):
    state_region_id = request.GET.get('stage_region_id')
    #state_region_id = id
    #township_id_list = list(SiteLocation.objects.filter(is_active=True).values_list("township_id",flat=True).distinct())
    print(f"this is stage_region_id from load townships {state_region_id}")
    townships = Township.objects.filter(state_region__id = state_region_id).order_by('name')
    # townships = Township.objects.filter(state_region__id = state_region_id).order_by('name')
    # return JsonResponse({'townships': list(townships.values('id', 'name'))})
    return JsonResponse(list(townships.values('id', 'name')),safe=False)

@login_required
def load_addresses(request):
    township_id = request.GET.get('township_id')
    state_region_id = request.GET.get('stage_region_id')
    site_locations = SiteLocation.objects.filter(state_region__id = state_region_id, township__id = township_id)
    return JsonResponse(list(site_locations.values('id', 'site_address', 'site_address_mm')),safe=False)

@login_required
def load_clinic(request):
    site_location_id = request.GET.get('site_location_id')
    site_location = SiteLocation.objects.filter(id=site_location_id)
    return JsonResponse(list(site_location.values('id', 'clinic_name', 'clinic_name_mm', 'channel__name', 'organization__name')),safe=False)

# @login_required
# def add_additional_ph(request, id):

#     client = get_object_or_404(Client, id=id)

#     if request.method == 'POST':
#         form = AdditionalPhoneForm(request.POST)
#         if form.is_valid():

#             form.save(client=client)

#             # Redirect to the success page
#             return redirect('client_details', id=id)
#     else:
#         form = AdditionalPhoneForm()

#     return render(request, 'callcenter/client_additional_ph.html', {'form': form})

@login_required
def add_additional_ph(request, id):

    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        print(request.POST)
        form = AdditionalPhoneForm(request.POST)
        if form.is_valid():
            new_phone = form.save(client=client)
            print("Form is valid and data has been saved.")
            return JsonResponse({'success': True, 'new_phone': new_phone.phone_number})
        else:
            # manually construct error message without field name
            error_message = ""
            for field in form.errors:
                error_message += form.errors[field][0]
            return JsonResponse({'success': False, "error_message": error_message})
    else:
        return JsonResponse({"error": "Invalid request"})


# @login_required
# def reach_info(request, id):

#     client = get_object_or_404(Client, id=id)

#     if request.method == 'POST':
#         form = ReachInfoForm(request.POST)
#         if form.is_valid():
#             form.save(client=client)
#             return redirect('client_details', id=id)
#     else:
#         form = ReachInfoForm()

#     return render(request, 'callcenter/client_reach_info.html', {'form':form})

@login_required
def reach_info(request, id):

    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        form = ReachInfoForm(request.POST)
        if form.is_valid():
            form.save(client=client)
            return JsonResponse({
                'success': True,
                'is_reached': form.cleaned_data['is_reach'],
                'reach_date': form.cleaned_data['reached_date'],
            })
        else:
            # If form is invalid, return a JSON response with an error message
            return JsonResponse({
                'success': False,
                'error': form.errors,
            })


@login_required
def get_investigation_types(request):
    investigation_types = InvestigationType.objects.all().order_by('type_description')
    response_data = list(investigation_types.values('id', 'type_description'))
    return JsonResponse(response_data, safe=False)

@login_required
def get_investigation_results(request, investigation_type_id):
    investigation_results = InvestigationResult.objects.filter(investigation_type_id=investigation_type_id).order_by('result_description')
    response_data = list(investigation_results.values('id', 'result_description'))
    return JsonResponse(response_data, safe=False)


# @login_required
# def taken_investigations(request, id):

#     client = get_object_or_404(Client, id=id)

#     if request.method == 'POST':
#         form = InvestigationForm(request.POST)
#         if form.is_valid():
#             form.save(client=client)
#             return redirect('client_details', id=id)
#     else:
#         form = InvestigationForm()

#     return render(request, 'callcenter/client_taken_investigations.html', {'form':form})

@login_required
def taken_investigations(request, id):

    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        form = InvestigationForm(request.POST)
        if form.is_valid():
            result = form.save(client=client)
            return JsonResponse({
                'success': True,
                'investigation_type': result.taken_investigation_type.type_description,
                'investigation_result': result.taken_investigation_result.result_description,
                'investigation_date': result.taken_investigation_date,
            })
        else:
            # If form is invalid, return a JSON response with an error message
            return JsonResponse({
                'success': False,
                'error': form.errors,
            })
    else:
        return JsonResponse({"error": "Invalid request"})


@login_required
def load_investigation_results(request):
    investigation_type_id = request.GET.get('investigation_type_id')
    investigation_type = InvestigationResult.objects.filter(investigation_type_id=investigation_type_id)
    return JsonResponse(list(investigation_type.values('id', 'result_description')),safe=False)


@login_required
def tb_confirmation(request, id):

    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        form = TBConfirmationForm(request.POST)
        if form.is_valid():
            result = form.save(client=client)
            return JsonResponse({
                'success': True,
                'is_bat_confirmed': result.is_bat_confirmed,
                'tb_diagnosis': result.tb_diagnosis,
                'diagnosis_date': result.diagnosis_date,
            })
        else:
            # If form is invalid, return a JSON response with an error message
            return JsonResponse({
                'success': False,
                'error': form.errors,
            })

    else:
        return JsonResponse({"error": "Invalid request"})


@login_required
def get_tb_regimes(request):
    regimes = TxRegime.objects.filter(is_active=True)
    response_data = list(regimes.values('id', 'type'))
    return JsonResponse(response_data, safe=False)


# @login_required
# def tb_treatment(request, id):

#     client = get_object_or_404(Client, id=id)

#     if request.method == 'POST':
#         form = TBTreatmentForm(request.POST)
#         if form.is_valid():
#             form.save(client=client)
#             return redirect('client_details', id=id)

#     else:
#         form = TBTreatmentForm()

#     return render(request, 'callcenter/client_tb_treatment.html', {'form':form})


@login_required
def tb_treatment(request, id):

    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        form = TBTreatmentForm(request.POST)
        if form.is_valid():
            result = form.save(client=client)
            return JsonResponse({
                'success': True,
                'is_registered_for_tx': result.is_registered_for_tx,
                'tx_regime': result.tx_regime.type,
                'registered_date': result.registered_date,
                'is_same_as_referred_site': result.is_same_as_referred_site
            })
        else:
            # If form is invalid, return a JSON response with an error message
            return JsonResponse({
                'success': False,
                'error': form.errors,
            })

    else:
        return JsonResponse({"error": "Invalid request"})


# def load_channel(request):
#     site_location_id = request.GET.get('site_location_id')
#     site_location = SiteLocation.objects.get(id=site_location_id)
#     return JsonResponse(list(site_location.values('id', 'channel__name')),safe=False)


# def load_organization(request):
#     site_location_id = request.GET.get('site_location_id')
#     site_location = SiteLocation.objects.get(id=site_location_id)
#     return JsonResponse(list(site_location.values('id', 'organization__name')),safe=False)


# def load_available_sites(request):
#     state_region_id = request.GET.get('site_id')
#     township_id = request.GET.get('township')
#     sites = SiteLocation.objects.filter(township__id=township_id,state_region__id=state_region_id)
#     return JsonResponse({'sites': list(sites.values('id', 'site_address'))})
# views.py - Example only
# /use-coupon/?coupon_code=COUPONTEST01

# from django.contrib.auth.models import User
# from django.http import HttpResponse

# from coupon_management.validations import validate_coupon
# from coupon_management.models import Coupon
# from django.views import View

# class UseCouponView(View):
#     def get(self, request, *args, **kwargs):
#         coupon_code = request.GET.get("coupon_code")
#         user = User.objects.get(username=request.user.username)

#         status = validate_coupon(coupon_code=coupon_code, user=user)
#         if status['valid']:
#             coupon = Coupon.objects.get(code=coupon_code)
#             coupon.use_coupon(user=user)

#             return HttpResponse("OK")

#         return HttpResponse(status['message'])