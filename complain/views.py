# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render, redirect

from complain.models import Govt_Agency_Access
from .models import Complain, Govt_Agency
import random
from .forms import UserForm, LoginForm, ComplainForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.template.context_processors import csrf
from .utils import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def mobile_index(request):
    table = "<input type='hidden' name='csrfmiddlewaretoken' value='" + str(csrf(request)['csrf_token']) + "'>";
    return render(request, 'mobile/index.html', {})

@csrf_exempt
def mobile_complain(request):
    if request.method == 'POST':
        form = ComplainForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        #return redirect('/mobile/index')
        return JsonResponse({'status':'ok'})
    #forms = ComplainForm()
    #return render(request, 'mobile/send_report.html', {"forms":forms})
    return JsonResponse({'form':form_1(request)})

def complains_list(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        agency = request.POST['agency']
        message = request.POST['message']
        code = genCode()
        agncy = Govt_Agency.objects.get(name=agency)
        n_comp = Complain(code=code, subject=subject, govt_agency=agncy, message=message)
        n_comp.save()
        return redirect('/complain/' + str(code))

    govt_agency = Govt_Agency.objects.all()
    complains = Complain.objects.all()
    context = {
        'complains': complains,
        'agencies': govt_agency
    }
    return render(request, "index.html", context)


def check_status(request):
    if request.method == 'POST':
        code = request.POST['code']
        # return redirect('/complain/'+str(code))
        govt_agency = Govt_Agency.objects.all()
        complain = Complain.objects.filter(code=code)
        context = {
            'complain': complain,
            'agencies': govt_agency
        }
        return render(request, "status.html", context)
    else:
        return redirect('/complain/')


def complains_status(request, pk):
    govt_agency = Govt_Agency.objects.all()
    complain = Complain.objects.get(code=pk)
    context = {
        'complain': complain,
        'agencies': govt_agency
    }
    return render(request, "status.html", context)


def genCode():
    rndm = random.randint(1, 1001) * 5

    cmpln = Complain.objects.filter(code=rndm).count()
    if cmpln > 0:
        genCode()
    else:
        return rndm


###agency
def register_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.save()
            authenticate(username=form_obj.username, password=form_obj.password)
            return HttpResponse('contact site admin for activation thank you for signing up')
    else:
        form = UserForm()
    # return render(request, 'register_user.html',{'form':form})
    return render(request, "agency/signup.html", {'form':form})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/agency/')
        else:
            return HttpResponse("login error.")
    else:
        form = LoginForm()
    # return render(request, 'login.html',{'form':form})
    return redirect('/complain/')


def login_out(request):
    logout(request)
    return redirect('/agency/')

# agency list
def agency_complains_list(request):
    if request.user.is_authenticated():
        gov = Govt_Agency_Access.objects.get(user = request.user)
        gov = Govt_Agency.objects.get(id=gov.agency.id)
        complains = Complain.objects.filter(govt_agency=gov)
        context={"complains":complains,
                 "gov":gov}
        return render(request, "agency/index.html", context)
    else:
        return render(request, "agency/login.html")
