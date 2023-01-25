from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer
from django.contrib.auth.models import User, Group


def index(request):
    context = {
        'abc': 'abc',
    }
    return render(request,'callcenter/index.html',context)

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