from django.db import models
import uuid
from django.utils import timezone
#import datetime
# Create your models here.

CHANNEL_NAME_CHOICES = [('Public', 'Public'),('Private', 'Private')]


class BaseModel(models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

#STAGE_CHOICE = [('1','Stage1ChatbotCompletion'),('2','Stage1Contact'),('3','Stage1TBReferral'),('4','')]
class Stage(BaseModel):
    description = models.CharField(max_length=255,null=False)

    class Meta:
        verbose_name_plural = "01. Stages"
    def __str__(self):
        return f'{self.description}'

# class Case(BaseModel):
#     #case_id = models.BigAutoField(primary_key=True,editable=False)
#     #case_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
#     #stage = models.CharField(max_length=1,choices=STAGE_CHOICE)
#     stage_id = models.ForeignKey(Stage,on_delete=models.PROTECT)

CLIENT_TYPE_CHOICE = [('Self','Self'),('Family','Family')]
GENDER_CHOICE = [('Male','Male'),('Female','Female'),('Other','Other')]
AGE_RANGE_CHOICE = [('BelowFifteen','BelowFifteen'),('FifteenAndAbove','FifteenAndAbove')]
class Client(BaseModel):
    type = models.CharField(max_length=255,null=False,choices=CLIENT_TYPE_CHOICE)
    gender = models.CharField(max_length=255,null=False,choices=GENDER_CHOICE)
    #gender = models.ForeignKey(Gender,on_delete=models.CASCADE)
    age_range = models.CharField(max_length=255,null=False,choices=AGE_RANGE_CHOICE)
    stage = models.ForeignKey(Stage,on_delete=models.PROTECT,default=1)

    def __str__(self):
        return f"{self.id} {self.type} {self.gender} {self.age_range}"

class ChatbotClient(BaseModel):
    social_media_id = models.CharField(max_length=255,null=False)
    social_media_name = models.CharField(max_length=255,null=False)
    client = models.ForeignKey(Client,on_delete=models.PROTECT,null=True)

class TBReferralClient(BaseModel):
    name = models.CharField(max_length=255,null=False)
    age_range = models.CharField(max_length=255,null=True,choices=AGE_RANGE_CHOICE)
    client = models.ForeignKey(Client,on_delete=models.PROTECT)

PHONE_TYPE_CHOICE = [('1','Primary'),('2','Additional')]
class ClientPhone(BaseModel):
    phone_number = models.CharField(max_length=255,null=False)
    phone_type = models.CharField(max_length=255,null=False,choices=PHONE_TYPE_CHOICE,default='1')
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    can_be_contacted = models.BooleanField(null=True,blank=True)

QUESTION_TYPE_CHOICE = [('c','Child'),('a','Adult')]
class SymptomQuestion(BaseModel):
    description = models.CharField(max_length=255,null=False)
    type = models.CharField(max_length=1,null=False,choices=QUESTION_TYPE_CHOICE)
    is_active = models.BooleanField()

    class Meta:
        verbose_name_plural = "02. Symptom questions"

    def __str__(self):
        return f"{self.id} {self.description}"

class ClientSymptomQuestionAnswer(BaseModel):
    question = models.ForeignKey(SymptomQuestion,on_delete=models.PROTECT)
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    answer = models.BooleanField()
    stage = models.ForeignKey(Stage,on_delete=models.PROTECT)

class ClientTBReferral(BaseModel):
    is_willing_to_be_referred = models.BooleanField()
    client = models.ForeignKey(Client,on_delete=models.PROTECT)

class CallAttempt(BaseModel):
    count = models.PositiveSmallIntegerField()
    current_attempt_date = models.DateField()
    next_attempt_date = models.DateField()
    stage = models.ForeignKey(Stage,on_delete=models.PROTECT)
    client =models.ForeignKey(Client,on_delete=models.PROTECT)

class SocialPlatform(BaseModel):
    name = models.CharField(max_length=255,null=False)

    class Meta:
        verbose_name_plural = "03. Social platforms"

    def __str__(self):
        return f"{self.name}"

class ClientSocialPlatform(BaseModel):
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    social_platform = models.ForeignKey(SocialPlatform,on_delete=models.PROTECT)
    is_active = models.BooleanField()

class StateRegion(BaseModel):
    name = models.CharField(max_length=255,null=False)

    class Meta:
        verbose_name_plural = "04. States regions"

    def __str__(self):
        return f"{self.name}"

class Township(BaseModel):
    name = models.CharField(max_length=255,null=False)
    name_mm = models.CharField(max_length=255,null=False,default="")
    state_region = models.ForeignKey(StateRegion,on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "05. Townships"

    def __str__(self):
        return f"{self.name}"

class Channel(BaseModel):
    name = models.CharField(max_length=255,null=False)

    class Meta:
        verbose_name_plural = "06. Channels"

    def __str__(self):
        return f"{self.name}"

class Organization(BaseModel):
    name = models.CharField(max_length=255,null=False)

    class Meta:
        verbose_name_plural = "07. Organizations"

    def __str__(self):
        return f"{self.name}"

SITE_TYPE_CHOICE = [('1','Referral'),('2','Register')]
class SiteLocation(BaseModel):
    is_active = models.BooleanField(null=False)
    state_region = models.ForeignKey(StateRegion,on_delete=models.PROTECT)
    township = models.ForeignKey(Township,on_delete=models.PROTECT)
    channel = models.ForeignKey(Channel,on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization,on_delete=models.PROTECT)
    clinic_name = models.CharField(max_length=255,null=True,blank=True)
    clinic_name_mm = models.CharField(max_length=255,null=True,blank=True)
    site_address = models.CharField(max_length=255,null=False)
    site_address_mm = models.CharField(max_length=255,null=True)
    provider_name = models.CharField(max_length=255,null=True)
    provider_name_mm = models.CharField(max_length=255,null=True)
    site_type = models.CharField(max_length=255,null=False,choices=SITE_TYPE_CHOICE)


    class Meta:
        verbose_name_plural = "08. SiteLocations"

    def __str__(self):
        return f"{self.clinic_name} {self.clinic_name_mm} {self.site_address} {self.site_address_mm} {self.site_type} {self.organization_id} {self.channel_id} {self.township_id} {self.state_region_id}"
# class RegisterSiteLocation(BaseModel):
#     is_active = models.BooleanField(null=False)
#     state_region_id = models.ForeignKey(StateRegion,on_delete=models.PROTECT)
#     township_id = models.ForeignKey(Township,on_delete=models.PROTECT)
#     channel_id = models.ForeignKey(Channel,on_delete=models.PROTECT)
#     organization_id = models.ForeignKey(Organization,on_delete=models.PROTECT)
#     site_name = models.CharField(max_length=255,null=False)

ACTION_TYPE_CHOICE = [('1','Referral'),('2','Register')]
class ClientRefRegLocation(BaseModel):
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    site_location = models.ForeignKey(SiteLocation,on_delete=models.PROTECT)
    action_date = models.DateField()
    action_type = models.CharField(max_length=1,null=False,choices=ACTION_TYPE_CHOICE)

class ClientReachInfo(BaseModel):
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    is_reached_to_referral_site = models.BooleanField(null=False)
    reached_date = models.DateField(null=False)
#    referred_location = models.ForeignKey(ClientRefRegLocation,on_delete=models.PROTECT)

class InvestigationType(BaseModel):
    type_description = models.CharField(max_length=255,null=False)

    class Meta:
        verbose_name_plural = "09. InvestigationTypes"

    def __str__(self):
        return f"{self.type_description}"


RESULT_TYPE_CHOICE = [('Positive','Positive'),('Negative','Negative')]
class InvestigationResult(BaseModel):
    result_description = models.CharField(max_length=255,null=False)
    result_type = models.CharField(max_length=255,null=False,choices=RESULT_TYPE_CHOICE,default="")
    investigation_type = models.ForeignKey(InvestigationType,on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "10. InvestigationResults"

    def __str__(self):
        return f"{self.result_description}"

class ClientInvestigatedResult(BaseModel):
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    taken_investigation_type = models.ForeignKey(InvestigationType,on_delete=models.PROTECT)
    taken_investigation_result = models.ForeignKey(InvestigationResult,on_delete=models.PROTECT)
    taken_investigation_date = models.DateField(null=False)

    class Meta:
        ordering = ['-taken_investigation_date']

TB_DIAGNOSIS_CHOICE = [('Positive','Positive'),('Negative','Negative')]
class ClientTBConfirmation(BaseModel):
    is_bat_confirmed = models.BooleanField(null=False)
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    tb_diagnosis = models.CharField(max_length=8,choices=TB_DIAGNOSIS_CHOICE)
    diagnosis_date = models.DateField(null=False)

class TxRegime(BaseModel):
    type = models.CharField(max_length=255,null=False)
    is_active = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.type}'

    class Meta:
        verbose_name_plural = "11. TxRegimes"

class ClientTBTreatment(BaseModel):
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    is_registered_for_tx = models.BooleanField()
    is_same_as_referred_site = models.BooleanField(null=True)
    # tx_regime = models.CharField(max_length=255,null=False)
    tx_regime = models.ForeignKey(TxRegime,on_delete=models.PROTECT)
    registered_date = models.DateField(null=False,default=timezone.now)


