from django.shortcuts import render, redirect, render_to_response
from django.http import *
from django.template import RequestContext
from django.template.response import TemplateResponse
from privateviews.decorators import login_not_required
from django.forms.util import ErrorList
from forms import *
from models import *

from django.contrib.auth import authenticate, login, logout

@login_not_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_not_required 
def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.POST.get('next'))
    return render_to_response('login.html', context_instance=RequestContext(request))
 


def index(request):
    events = Event.objects.all().order_by('-id')
    pictures = Picture.objects.all()
    
    return TemplateResponse(request, 'base.html', {'events':events})


def upload(request):
    
    if request.POST:
        
        form = UploadFileForm(request.POST, request.FILES, prefix="upload")
        sub_form = EventForm(request.POST, prefix="event")
        
        if sub_form.is_valid():
            try:
                form.is_valid()
            except:
                pass
            if form.errors:
                return TemplateResponse(request, 'upload.html', {'form': form, 'sub_form': sub_form})
               
            if form.cleaned_data['event']:
                upload = form.save()
                upload.extract()
                return redirect(index)
    
            elif sub_form.cleaned_data['name']:
                event = sub_form.save()
                if form.is_valid():
                    upload = form.save(commit=False)
                    file = request.FILES['upload-file']
                    upload.event = event
                    upload.file = file
                    upload.save()
                    upload.extract()
                    #form.save(event=event)
                    return redirect(index)
                    
            else:
                errors = form._errors.setdefault("event", ErrorList())
                errors.append(u"You must select an event or create a new one")
                return TemplateResponse(request, 'upload.html', {'form': form, 'sub_form': sub_form})
        else:
            return TemplateResponse(request, 'upload.html', {'form': form, 'sub_form': sub_form})

    else:
        
        form = UploadFileForm(prefix="upload")
        sub_form = EventForm(prefix="event")
    
    return TemplateResponse(request, 'upload.html', {'form': form, 'sub_form': sub_form})