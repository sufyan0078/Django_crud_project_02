from typing import Any
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import StudentRegistration
from .models import User
from django.views.generic.base import View,TemplateView,RedirectView


class AddAndShow(TemplateView):
    template_name = "enroll/addandshow.html"
    def get_context_data(self,*args, **kwargs):
        context =  super().get_context_data(**kwargs)
        fm = StudentRegistration()
        data = User.objects.all()
        context = {'stu':data,'form':fm}
        return context
    def post(self,request):
        fm = StudentRegistration(request.POST)
        if fm.is_valid():
          nm = fm.cleaned_data["name"]
          em = fm.cleaned_data["email"]
          pw = fm.cleaned_data["password"]
          reg = User(name=nm,email=em,password=pw)
          reg.save()
          fm = StudentRegistration()
        return HttpResponseRedirect('/')


class UpdateView(View):
    def get(self, request, id):
        data = User.objects.get(pk=id)
        fm = StudentRegistration(instance=data)
        return render(request,"enroll/updatestudent.html",{"form":fm})
    def post(self, request, id):
        data = User.objects.get(pk=id)
        fm = StudentRegistration(request.POST, instance=data)
        if fm.is_valid():
            fm.save()
        return render(request,"enroll/updatestudent.html",{"form":fm})
        
class DelDataView(RedirectView):
    url = '/'
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        id = kwargs['id']
        User.objects.get(pk=id).delete()
        return super().get_redirect_url(*args, **kwargs)



