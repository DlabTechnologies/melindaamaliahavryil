from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import UserContactForm, SendEmailForm, UserNewsletterSignup
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from account.models import ManagerContactInfo, RecentPayouts, Account_level, NewsletterSignup
from django.contrib.auth.decorators import login_required



def home_page(request):

        if request.user.is_authenticated:
                if not request.user.is_admin:
                        return redirect('user_dashboard')
        

                
    

        info = ManagerContactInfo.objects.all()

        
        form = UserContactForm()
        if request.method == 'POST':
                form = UserContactForm(request.POST)
                if form.is_valid():
                        form.save()
                        name = form.cleaned_data.get('name')
                        email = form.cleaned_data.get('email')
                        subject = form.cleaned_data.get('subject')
                        #code = form.cleaned_data.get('code')
                        phone = form.cleaned_data.get('phone')
                        
                        

                        messages.success(request, 'Message sent successfully')
                        return redirect('home_page')
                        
        else:
                form = UserContactForm()

       
        context={
                'form': form,
                'info': info,
                
        }
        return render(request, 'account/index.html', context)


def about_page(request):

        
        info = ManagerContactInfo.objects.all()

        context={
                'info': info
        }
        return render(request, 'account/about.html', context)


def resources_page(request):
       

        info = ManagerContactInfo.objects.all()

       
        context = {
                'info': info,
                
        }
        return render(request, 'account/resources.html', context)



#@login_required(login_url='login')
#def SendEmail(request):
        
       # form = SendEmailForm()
       # if request.method == 'POST':
         #       form = SendEmailForm(request.POST)
           #     if form.is_valid():
                   #     to = form.cleaned_data.get('to')
            #            subject = form.cleaned_data.get('subject')
                  #      message = form.cleaned_data.get('message')
            
                        
                    #    recipient_list = [to,]    
                     #   send_mail( subject, message, 'Cryptocurrencyinvestorsllc noreply@Cryptocurrencyinvestorsllc.com', recipient_list )    
                    #    messages.success(request, 'Message successfully sent to {}'.format(to))
                     #   return redirect('send_email')
            
      #  else:
       #         form = SendEmailForm()
       # context ={
        #        'form': form
       # }
       # return render (request, 'send_user_email.html', context)