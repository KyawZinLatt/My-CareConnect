from django.db import models
import uuid
# Create your models here.

CHANNEL_NAME_CHOICES = [('Public', 'Public'),('Private', 'Private')]

class Client(models.Model):
    case_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    phone_number = models.CharField(max_length=11,null=False)
    class Meta:
        abstract = True

class Question(models.Model):
    question = models.CharField(max_length=255,null=False)
    question_type = models.CharField(max_length=255,choices=[('Adult','Adult'),('Child','Child')],null=False)
class Gender(models.Model):
    gender_description = models.CharField(max_length=255,null=False)

class ChatbotClientDemo(Client):
    social_media_id = models.IntegerField(null=False)
    social_media_name = models.CharField(max_length=255,null=False)
    gender = models.ForeignKey(to=Gender,on_delete=models.CASCADE)
    age_range = models.CharField(max_length=255,choices=[('<15','<15'),('>=15','>=15')])

class ReferralClient(Client):
    name = models.CharField(max_length=255,null=False)
    sex = models.CharField(max_length=255,choices=[('Male','Male'),('Female','Female')])
    age_range = models.CharField(max_length=255,choices=[('<15','<15'),('>=15','>=15')])

class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=11)
    can_contact = models.BooleanField(null=True)
    type = models.CharField(max_length=255,choices=[('Primary','Primary'),('Additional','Additionalg')] )

class TBReferral(models.Model):
    referral_id = models.UUIDField(primary_key=True)

class StageOne(models.Model):
    referral_id = models.OneToOneField(TBReferral,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11)
    social_media_id = models.IntegerField()
    social_media_name = models.CharField(max_length=255)
    self_screening_date = models.DateField()
    user_type = models.CharField(max_length=255,choices=[('Self','Self'),('OnBehalf','OnBehalf')])
    sex = models.CharField(max_length=255,choices=[('Male','Male'),('Female','Female')])
    age_range = models.CharField(max_length=255,choices=[('<15','<15'),('>=15','>=15')])
    chatbot_aq_one = models.BooleanField()
    chatbot_aq_two = models.BooleanField()
    chatbot_aq_three = models.BooleanField()
    chatbot_aq_four = models.BooleanField()
    chatbot_aq_five = models.BooleanField()
    chatbot_aq_six = models.BooleanField()
    chatbot_aq_seven = models.BooleanField()
    chatbot_aq_eight = models.BooleanField()
    chatbot_cq_one = models.BooleanField()
    chatbot_cq_two = models.BooleanField()
    chatbot_cq_three = models.BooleanField()
    is_tb_suspected = models.BooleanField()
    call_attempt_count = models.SmallIntegerField()
    call_attempt_date = models.DateField()
    next_attempt_date = models.DateField()
    can_be_contacted = models.BooleanField()
    client_age_range = models.CharField(max_length=255,choices=[('<15','<15'),('>=15','>=15')])
    client_aq_one = models.BooleanField()
    client_aq_two = models.BooleanField()
    client_aq_three = models.BooleanField()
    client_aq_four = models.BooleanField()
    client_aq_five = models.BooleanField()
    client_aq_six = models.BooleanField()
    client_aq_seven = models.BooleanField()
    client_aq_eight = models.BooleanField()
    client_cq_one = models.BooleanField()
    client_cq_two = models.BooleanField()
    client_cq_three = models.BooleanField()
    willing_to_be_referred = models.BooleanField()
    client_name = models.CharField(max_length=255)
    is_viber_number = models.BooleanField()
    is_telegram_number = models.BooleanField()
    is_whatsapp_number = models.BooleanField()
    extra_phone_number = models.CharField(max_length=11)
    township = models.CharField(max_length=255)
    referral_channel_name = models.CharField(max_length=255,choices=CHANNEL_NAME_CHOICES)
    referral_org_name = models.CharField(max_length=255,choices=[('PSI','PSI'),('MAM','MAM')])
    referral_site_name = models.CharField(max_length=255,choices=[('Clinic A','Clinic A'),('MAM','MAM')])
    referral_date = models.DateField()

class StageTwo(models.Model):
    pass

class AdultQuestionAnswers(models.Model):
    aq_one = models.BooleanField()
    aq_two = models.BooleanField()
    aq_three = models.BooleanField()
    aq_four = models.BooleanField()
    aq_five = models.BooleanField()
    aq_six = models.BooleanField()
    aq_seven = models.BooleanField()
    aq_eight = models.BooleanField()

class Date(models.Model):
    my_date = models.DateField(null=False)
