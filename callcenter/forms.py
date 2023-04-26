from django import forms
from django.core.validators import RegexValidator
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, DatePickerInput
from django.forms.widgets import TextInput, Textarea
from callcenter.models import TxRegime, ClientTBTreatment, ClientTBConfirmation, ClientInvestigatedResult, InvestigationResult, InvestigationType, ClientReachInfo, ClientPhone, StateRegion, Township, Client, TBReferralClient, SymptomQuestion, ClientSymptomQuestionAnswer, Stage, ClientTBReferral, SocialPlatform, ClientSocialPlatform, ClientRefRegLocation, SiteLocation
#from django_bootstrap5.widgets import BootstrapTextInput, BootstrapTextarea


class StageFilterForm(forms.Form):
    stage = forms.ModelChoiceField(
        queryset=Stage.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)


# class ContactForm(forms.Form):
#     name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Enter your name'}))
#     email = forms.EmailField(widget=TextInput(attrs={'placeholder': 'Enter your email'}))
#     message = forms.CharField(widget=Textarea(attrs={'placeholder': 'Enter your message'}))

AGE_RANGE_CHOICE = [('','Select Age Range'), ('BelowFifteen','BelowFifteen'),('FifteenAndAbove','FifteenAndAbove')]
class FirstContactForm(forms.Form):

    # name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # email = forms.EmailField(max_length=100, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # message = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    hidden_client_id = forms.CharField(widget=forms.HiddenInput)
    can_contact = forms.ChoiceField(choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    age_range = forms.ChoiceField(choices=AGE_RANGE_CHOICE, required=True, widget=forms.Select(attrs={'class': 'form-control'}))


    def save(self, id=None, client_phone=None, ):

        if id:
            client = Client.objects.get(id=id)

        tb_referral_client_data = {
            'client': client,
            'age_range': self.cleaned_data['age_range'],
            }

        client_phone_data = {
            'can_be_contacted': self.cleaned_data['can_contact'],
            }

        if client_phone:
            for field, value in client_phone_data.items():
                setattr(client_phone, field, value)
            client_phone.save()

        tb_referral_client = TBReferralClient.objects.filter(client=client)
        if tb_referral_client:
            for field, value in tb_referral_client_data.items():
                setattr(tb_referral_client, field, value)
            tb_referral_client.save()
        else:
            tb_referral_client = TBReferralClient.objects.create(**tb_referral_client_data)
        #print(tb_referral_client.id)


        client_phone.client = client
        client_phone.save()
        tb_referral_client.client = client
        tb_referral_client.save()
        # latest_call = CallAttempt.objects.filter(client=client).order_by('-id').first()
        # if latest_call:

        # call_log_data = {
        #     'count':
        # }
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if not email.endswith('@example.com'):
    #         raise forms.ValidationError('Invalid email address. Please use a valid example.com email address.')
    #     return email

    # def clean_message(self):
    #     message = self.cleaned_data['message']
    #     if len(message) < 10:
    #         raise forms.ValidationError('Message is too short. Please enter a message with at least 10 characters.')
    #     return message


class SymptomByCallAdultForm(forms.Form):

    adult_symptom_questions = SymptomQuestion.objects.filter(is_active=True,type='a')

    question1 = forms.ChoiceField(label=adult_symptom_questions[0].description,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    question2 = forms.ChoiceField(label=adult_symptom_questions[1].description,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    question3 = forms.ChoiceField(label=adult_symptom_questions[2].description,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    question4 = forms.ChoiceField(label=adult_symptom_questions[3].description,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    question5 = forms.ChoiceField(label=adult_symptom_questions[4].description,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    question6 = forms.ChoiceField(label=adult_symptom_questions[5].description,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    question7 = forms.ChoiceField(label=adult_symptom_questions[6].description,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    question8 = forms.ChoiceField(label=adult_symptom_questions[7].description,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))



    def save(self, client=None):
        adult_symptom_questions = SymptomQuestion.objects.filter(is_active=True,type='a')
        stage = Stage.objects.get(id=2)
        questions_answers = []
        for i in range(1, 9):
            client_question_answer = ClientSymptomQuestionAnswer(
                answer = self.cleaned_data[f'question{i}'],
                question = adult_symptom_questions[i-1],
                stage = stage,
                client = client
                )
            questions_answers.append(client_question_answer)
        ClientSymptomQuestionAnswer.objects.bulk_create(questions_answers)
        client_data = {
            'stage': stage
            }
        if client:
            for field, value in client_data.items():
                setattr(client, field, value)
            client.save()


class SymptomByCallChildForm(forms.Form):

    child_symptom_questions = SymptomQuestion.objects.filter(is_active=True,type='c')

    question1 = forms.ChoiceField(label=child_symptom_questions[0].description,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    question2 = forms.ChoiceField(label=child_symptom_questions[1].description,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    question3 = forms.ChoiceField(label=child_symptom_questions[2].description,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))


    def save(self, client=None):
        child_symptom_questions = SymptomQuestion.objects.filter(is_active=True,type='c')
        stage = Stage.objects.get(id=2)
        questions_answers = []
        for i in range(1, 4):
            client_question_answer = ClientSymptomQuestionAnswer(
                answer = self.cleaned_data[f'question{i}'],
                question = child_symptom_questions[i-1],
                stage = stage,
                client = client
                )
            questions_answers.append(client_question_answer)
        ClientSymptomQuestionAnswer.objects.bulk_create(questions_answers)
        client_data = {
            'stage': stage
            }
        if client:
            for field, value in client_data.items():
                setattr(client, field, value)
            client.save()


class TBReferralForm(forms.Form):
    willing_to_be_referred = forms.ChoiceField(label="Willing to be referred?",choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(label="Name",max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def save(self, client=None):
        willing_to_be_referred_data = {
            'is_willing_to_be_referred': self.cleaned_data['willing_to_be_referred'],
            'client': client,
            }
        ClientTBReferral.objects.create(**willing_to_be_referred_data)

        name_data = {
            'name': self.cleaned_data['name']
            }
        tb_referral_client = client.tbreferralclient_set.all().first()
        for field, value in name_data.items():
            setattr(tb_referral_client, field, value)
        tb_referral_client.save()


class ActiveSocialPlatformsForm(forms.Form):

    platforms = SocialPlatform.objects.all()

    platform1 = forms.ChoiceField(label=platforms[0].name,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    platform2 = forms.ChoiceField(label=platforms[1].name,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    platform3 = forms.ChoiceField(label=platforms[2].name,choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')), required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self, client=None):
        platforms = SocialPlatform.objects.all()
        client_social_platforms = []
        for i in range(1, 4):
            client_social_platform = ClientSocialPlatform(
                client = client,
                social_platform = platforms[i-1],
                is_active = self.cleaned_data[f'platform{i}'],
                )
            client_social_platforms.append(client_social_platform)
        ClientSocialPlatform.objects.bulk_create(client_social_platforms)



class ReferLocationForm(forms.Form):

    stage_region_id_list = list(SiteLocation.objects.filter(is_active=True).values_list("state_region_id",flat=True).distinct())
    unique_active_states_regions = SiteLocation.objects.filter(is_active=True).values_list("state_region_id","state_region__name").distinct()


    #refer_date = forms.DateField(label="Refer Date", required=True, widget=forms.DateInput(attrs={'class': 'form-control','type': 'date',}))
    refer_date = forms.DateField(
        label="Refer Date",
        required=True,
        widget=DatePickerInput(
            attrs = {'class': 'form-control'},
            options={
                "format": "DD/MMM/YYYY",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
                "allowInputToggle": True
            }
        )
    )

    state_region = forms.ModelChoiceField(
        label="State Region",
        queryset=StateRegion.objects.filter(id__in=stage_region_id_list).order_by('name'),
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'state-region-select',
                }
            )
    )
    #state_region = forms.ModelChoiceField(label="State Region",queryset=SiteLocation.objects.filter(is_active=True),widget=forms.Select(attrs={'class': 'form-control','id': 'state-region-select',}))
    township = forms.ModelChoiceField(
        queryset=Township.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'township-select',
            }
        )
    )
    #township = forms.ModelChoiceField(label="Township",queryset=SiteLocation.objects.none(),widget=forms.Select(attrs={'class': 'form-control','id': 'township-select',}))
    site = forms.ModelChoiceField(label="Site Address",queryset=SiteLocation.objects.none(),widget=forms.Select(attrs={'class': 'form-control','id': 'site-select',}))
    clinic = forms.ModelChoiceField(label="Clinic Name",queryset=SiteLocation.objects.none(),widget=forms.Select(attrs={'class': 'form-control','id': 'clinic-select',}))
    channel = forms.ModelChoiceField(label="Channel",queryset=SiteLocation.objects.none(),widget=forms.Select(attrs={'class': 'form-control','id': 'channel-select',}))
    organization = forms.ModelChoiceField(label="Organization",queryset=SiteLocation.objects.none(),widget=forms.Select(attrs={'class': 'form-control','id': 'organization-select',}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #print(self.instance)
        if 'state_region' in self.data:
            try:
                state_region_id = int(self.data.get('state_region'))
                #print(f"this is state_region_id kyaw -> {state_region_id}")
                self.fields['township'].queryset = Township.objects.filter(state_region_id=state_region_id).order_by('name')
            except (ValueError, TypeError):
                pass
        if 'township' in self.data:
            try:
                state_region_id = int(self.data.get('state_region'))
                township_id = int(self.data.get('township'))
                #print(f"this is township_id kyaw -> {township_id}")
                self.fields['site'].queryset = SiteLocation.objects.filter(state_region_id=state_region_id,township_id=township_id)
            except (ValueError, TypeError):
                pass
        if 'site' in self.data:
            try:
                site_id = int(self.data.get('site'))
                #print(f"this is township_id kyaw -> {township_id}")
                self.fields['clinic'].queryset = SiteLocation.objects.filter(id=site_id)
            except (ValueError, TypeError):
                pass
        if 'clinic' in self.data:
            try:
                site_id = int(self.data.get('clinic'))
                #print(f"this is township_id kyaw -> {township_id}")
                self.fields['channel'].queryset = SiteLocation.objects.filter(id=site_id)
            except (ValueError, TypeError):
                pass
        if 'channel' in self.data:
            try:
                site_id = int(self.data.get('channel'))
                #print(f"this is township_id kyaw -> {township_id}")
                self.fields['organization'].queryset = SiteLocation.objects.filter(id=site_id)
            except (ValueError, TypeError):
                pass

    def save(self, client=None):
        site_id = self.cleaned_data['site'].id
        print(f'type is ----> {type(site_id)}')
        site_location = SiteLocation.objects.get(id=site_id)
        client_ref_data = {
            'site_location': site_location,
            'client': client,
            'action_date': self.cleaned_data['refer_date'],
            'action_type': '1'
        }
        ClientRefRegLocation.objects.create(**client_ref_data)
        client.stage_id = 3
        client.save()


class ReachInfoForm(forms.Form):
    is_reach = forms.ChoiceField(
        label = "Is reached to Referral Site?",
        choices = (('', 'Select Answer'), (True, 'Yes'), (False, 'No')),
        required = True,
        widget = forms.Select(attrs={'class': 'form-control'})
    )

    reached_date = forms.DateField(
        label="Reached Date",
        required=True,
        widget=DatePickerInput(
            attrs={'class': 'form-control'},
            options={
                "format": "DD/MMM/YYYY",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
                "allowInputToggle": True
            }
        )
    )

    def save(self, client=None):
        reach_data = {
            'client': client,
            'is_reached_to_referral_site': self.cleaned_data['is_reach'],
            'reached_date': self.cleaned_data['reached_date'],
        }
        ClientReachInfo.objects.create(**reach_data)
        client.stage_id = 4
        client.save()


class InvestigationForm(forms.Form):

    investigation_type = forms.ModelChoiceField(
        label="Investigation Type",
        required=True,
        queryset=InvestigationType.objects.all().order_by('type_description'),
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'investigation-type-select',
                }
            )
    )

    investigation_result = forms.ModelChoiceField(
        label="Investigation Result",
        required=True,
        queryset=InvestigationResult.objects.none(),
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'investigation-result-select',
                }
            )
    )

    investigation_date = forms.DateField(
        label="Investigation Date",
        required=True,
        widget=DatePickerInput(
            attrs={'class': 'form-control'},
            options={
                "format": "DD/MMM/YYYY",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
                "allowInputToggle": True
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #print(self.instance)
        if 'investigation_type' in self.data:
            try:
                investigation_type_id = int(self.data.get('investigation_type'))
                #print(f"this is state_region_id kyaw -> {state_region_id}")
                self.fields['investigation_result'].queryset = InvestigationResult.objects.filter(investigation_type_id=investigation_type_id)
            except (ValueError, TypeError):
                pass

    def save(self, client=None):
        # investigation_type = InvestigationType.objects.get(id=self.cleaned_data['investigation_type'])
        investigation_data = {
            'client': client,
            'taken_investigation_type': self.cleaned_data['investigation_type'],
            'taken_investigation_result': self.cleaned_data['investigation_result'],
            'taken_investigation_date': self.cleaned_data['investigation_date'],
        }
        ClientInvestigatedResult.objects.create(**investigation_data)


class TBConfirmationForm(forms.Form):

    bat_confirmed = forms.ChoiceField(
        label="Is bat confirmed?",
        choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    tb_diagnosis = forms.ChoiceField(
        label="TB Diagnosis",
        choices=(('', 'Select Answer'), ('Positive', 'Positive'), ('Negative', 'Negative')),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    diagnosis_date = forms.DateField(
        label="Diagnosis Date",
        required=True,
        widget=DatePickerInput(
            attrs={'class': 'form-control'},
            options={
                "format": "DD/MMM/YYYY",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
                "allowInputToggle": True
            }
        )
    )

    def save(self, client=None):
        tb_confirm_data = {
        'is_bat_confirmed': self.cleaned_data['bat_confirmed'],
        'tb_diagnosis': self.cleaned_data['tb_diagnosis'],
        'client': client,
        'diagnosis_date': self.cleaned_data['diagnosis_date'],
        }
        ClientTBConfirmation.objects.create(**tb_confirm_data)
        client.stage_id = 5
        client.save()



class TBTreatmentForm(forms.Form):


    registered_date = forms.DateField(
        label="Register Date",
        required=True,
        widget=DatePickerInput(
            attrs = {'class': 'form-control'},
            options={
                "format": "DD/MMM/YYYY",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
                "allowInputToggle": True
            }
        )
    )

    is_registered_for_tx = forms.ChoiceField(
        label="Is registered for Tx?",
        required=True,
        choices=(('', 'Select Answer'), (True, 'Yes'), (False, 'No')),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # tx_regime = forms.CharField(
    #     label="Tx regime",
    #     max_length=100,
    #     required=True,
    #     widget=forms.TextInput(attrs={'class': 'form-control'})
    # )

    tx_regime = forms.ModelChoiceField(
        label="Tx regime",
        required=True,
        queryset=TxRegime.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control','id': 'site-select',})
    )


    def save(self, client=None):
        register_data = {
        'client': client,
        'is_registered_for_tx': self.cleaned_data['is_registered_for_tx'],
        'tx_regime': self.cleaned_data['tx_regime'],
        'registered_date': self.cleaned_data['registered_date'],
        }
        ClientTBTreatment.objects.create(**register_data)
        client.stage_id = 6
        client.save()


# class PhoneInput(forms.widgets.TextInput):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.validators.append(RegexValidator(
#             regex='^\+\d{11,13}$',
#             message='Enter a valid phone number (format: +XXXXXXXXXXX or +XXXXXXXXXXXX)'
#         ))
#         self.attrs.update({'class': 'form-control'})

class AdditionalPhoneForm(forms.Form):
    phone_number = forms.CharField(
        label="Phone Number",
        required=True,
        max_length=13,
        validators=[RegexValidator(
            regex='^\+\d{11,13}$',
            message='Enter a valid phone number (format: +959...)'
        )],
        widget=forms.TextInput(attrs={'type': 'tel', 'class': 'form-control', 'placeholder': '+959...'})
    )


    def save(self, client=None):
        client_additional_ph_data = {
            'phone_number': self.cleaned_data['phone_number'],
            'client': client,
            'phone_type': '2',
            }
        ClientPhone.objects.create(**client_additional_ph_data)



    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if 'state_region' in self.data:
    #         try:
    #             state_region_id = int(self.data.get('state_region'))
    #             self.fields['township'].queryset = Township.objects.filter(state_region__id=state_region_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass
    #     elif self.instance.pk:
    #         self.fields['township'].queryset = self.instance.state_region.township_set.order_by('name')

# from django import forms
# from .models import Question

# class QuestionForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         for question in Question.objects.all():
#             field_name = f'question_{question.id}'
#             self.fields[field_name] = forms.BooleanField(
#                 label=question.text,
#                 required=False
#             )

#     def save(self):
#         for name, value in self.cleaned_data.items():
#             if value:
#                 question_id = name.split('_')[-1]
#                 question = Question.objects.get(id=question_id)
#                 answer = question.answers.create(value=value)
#                 answer.save()
