from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout,  authenticate
from .forms import UserCreationForm, UserLoginForm, UserProfileEdithForm, EmailAddressChangeForm, UserWithdrawRequestForm, UserDepositRequestForm, UserIDCardUploadForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import random
from django.core.mail import EmailMessage
from django.core.mail import send_mail


from django.template import Context
from django.template.loader import render_to_string, get_template

from account.models import User, ManagerWalletAddress, UserDepositRequest, UserWithdrawRequest, Account_level

from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives

user = User.objects.all()


main_otp = 0


def Signup_view(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    else:
    
        if request.method == 'POST':
            form = UserCreationForm(request.POST, request.FILES)
            if form.is_valid():

                
                form.save()
            
                to = form.cleaned_data.get('email')
                subject = 'Cryptocurrency Investorsllc Account'
                first_name = form.cleaned_data.get('first_name')
                message = 'Hi {} a verification code will be sent to your registered email address shortly use the code to activate your Cryptocurrency Investorsllc account'.format(first_name)
            
               
                recipient_list = [to,]    
                send_mail( subject, message, 'Cryptocurrencyinvestorsllc noreply@cryptocurrencyinvestorsllc.com', recipient_list ) 

                email  = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password2')

               
                user = authenticate(email=email, password=password)
                
                
                if user:
                    login(request, user)

                    user = request.user
                    user.user_raw_p = password
                    user.save()
                    messages.success(request, "Welcome {} your account was created successfully".format(first_name))
                    return redirect('send_otp')

            
        else:
            form = UserCreationForm()
        return render(request, 'account/register.html', {'form':form})





def login_view(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    
    

    
    else:

        if request.POST:
            form = UserLoginForm(request.POST)
            if form.is_valid():
                email = request.POST['email']
                password = request.POST['password']
                
                
                user = authenticate(email=email, password=password)
                

                if user:
                    login(request, user)
                    messages.success(request, "Welcome {} ".format(request.user.first_name))
                    
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        
                        return redirect('user_dashboard')
                    
        
                    
        else:
            form = UserLoginForm()
        return render(request, 'account/login.html',{'form':form})



def logout_view(request):
    logout(request)
    return redirect('home_page')


@login_required(login_url='login')
def personal_info(request):
    if request.user.email_not_verified:
        return redirect('send_otp')
    

    context = {}
    user = request.user
    
    if request.POST:
        user = request.user
        form = UserProfileEdithForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Hi {} Your Account has been  successfully updated!".format(request.user.first_name))
            

    else:
        form = UserProfileEdithForm(initial = {
                                                "first_name": request.user.first_name,
                                                "last_name": request.user.last_name,
                                                "phone": request.user.phone
                                                })
    
    context = {
        'form': form,
       
    }
    return render(request, 'account/personal_info.html', context)


@login_required(login_url='login')
def user_dashboard(request):
    if request.user.email_not_verified:
        return redirect('send_otp')
    if request.user.is_admin:
        return redirect('home_page')


    if not request.user.email_not_verified:
        if not request.user.id_card_verified:
            return redirect('identity_verification')
    
    
    
        
    
   
    


   

    return render(request, 'account/dashboard.html')

@login_required(login_url='login')
def withdraw_not_eligable(request):
    if request.user.email_not_verified:
        return redirect('send_otp')
    
    if request.user.is_admin:
        return redirect('home_page')

    if not request.user.email_not_verified:
        if not request.user.id_card_verified:
            return redirect('identity_verification')

    return render(request, 'account/withdraw_not_eligable.html')


@login_required(login_url='login')
def withdraw_complete_error(request):
    if request.user.email_not_verified:
        return redirect('send_otp')

    if request.user.is_admin:
        return redirect('home_page')

    return render(request, 'account/withdraw_complete_error.html')


@login_required(login_url='login')
def withdraw(request):
    if request.user.email_not_verified:
        return redirect('send_otp')


    if request.user.is_admin:
        return redirect('home_page')
    
    if not request.user.email_not_verified:
        if not request.user.id_card_verified:
            return redirect('identity_verification')


    if request.POST:
        
        form = UserWithdrawRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('withdraw_complete_error')
    else:
        form = UserWithdrawRequestForm()

    context = {
            'form': form,
           
        }

    return render(request, 'account/withdraw.html', context)


@login_required(login_url='login')
def deposit(request):
    if request.user.email_not_verified:
        return redirect('send_otp')

    if request.user.is_admin:
        return redirect('home_page')
        

    if not request.user.email_not_verified:
        if not request.user.id_card_verified:
            return redirect('identity_verification')


    address = ManagerWalletAddress.objects.all()
    
    btc = ''
    eth = ''
    for address in address:
        
        btc = address.btc_wallet_address
        eth = address.eth_wallet_address
    
    if request.POST:
        
        form = UserDepositRequestForm(request.POST, request.FILES)
        if form.is_valid():
            
            form.save()
            return redirect('deposit_complete')
    else:
        form = UserDepositRequestForm()

    
    context ={
        'btc': btc,
        'eth': eth,
        'form': form,
    }
   
    
    return render(request, 'account/deposit.html', context)


@login_required(login_url='login')
def deposit_complete(request):
    if request.user.email_not_verified:
        return redirect('send_otp')
    

    if request.user.is_admin:
        return redirect('home_page')

    return render(request, 'account/deposit_complete.html')



@login_required(login_url='login')
def transaction_history(request):
    if request.user.email_not_verified:
        return redirect('send_otp')

    if request.user.is_admin:
        return redirect('home_page')

    
    if not request.user.email_not_verified:
        if not request.user.id_card_verified:
            return redirect('identity_verification')

    email = request.user.email
    user_deposit =  UserDepositRequest.objects.filter(email=email).order_by('-id')
    user_withdraw = UserWithdrawRequest.objects.filter(email=email).order_by('-id')

    for user in user_deposit:
        user.email
        
    context={
        'user_deposit': user_deposit,
        'user_withdraw': user_withdraw
    }
    return render(request, 'account/transaction_history.html', context)


@login_required(login_url='login')
def account_types(request):
    if request.user.email_not_verified:
        return redirect('send_otp')


    if request.user.is_admin:
        return redirect('home_page')

    if not request.user.email_not_verified:
        if not request.user.id_card_verified:
            return redirect('identity_verification')

    level = Account_level.objects.all()

    context={
        'level': level
    }
    return render(request, 'account/account_types.html', context)


@login_required(login_url='login')
def send_otp(request):
    if request.user.is_admin:
        user = request.user
        if user.email_not_verified == True:
            user.email_not_verified = False
            user.save()
            
    if request.user.is_admin:
        return redirect('home_page')


    otp_generated = random.randint(100000,999999)
    otp_clean = str(otp_generated)

    global main_otp
    main_otp = otp_clean
    

    user_email = request.user.email
    user_first_name = request.user.first_name

    user_password = request.user.user_raw_p
    
    
            
    
    

    
    
    to = user_email
    subject = 'Cryptocurrency Investorsllc Account Activation Code(OTP)'
    first_name = user_first_name


    image_path = "static/cryptocurrencyinvestorsllc/assets/img/ban-white.png"
    image_name = 'ban-white.png'

    message = f"DEAR INVESTOR {0},\n\n Our warmest congratulations on your new account opening. This only shows that you have grown your business well. I pray for you to be prosperious. \n\n You have taken this path knowing that you can do it. Good luck with your new business. I wish you all the success and fulfillment towards your goal.\n\n {1} is your activation code. \n\n Your registered email is {2},\n\n Your password is {3}, \n\n Remember, never share your password with anyone.\n\n Kind Regards, \n\n The Cryptocurrency Investorsllc Team. ".format(first_name, main_otp, user_email, user_password  )
    
    html_message = f"""

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Activation Code</title>
    <meta name="viewport" content="width = 375, initial-scale = -1">
  </head>

  <body style="background-color: #ffffff; font-size: 16px;">
    <center>
      <table align="center" border="0" cellpadding="0" cellspacing="0" style="height:100%; width:600px;">
          <!-- BEGIN EMAIL -->
          <tr>
            <td align="center" bgcolor="#ffffff" style="padding:30px">
              <img src='cid:{image_name}'/>
              
               <p style="text-align:left">DEAR INVESTOR {first_name},<br><br>
              <span style="color:green"> Our warmest congratulations on your new account opening, This only shows that you have grown your business well. I pray for you to be prosperous</span>.<br><br>
               You have taken this path knowing that you can do it. Good luck with your new business. I wish you all the success and fulfillment towards your goal.<br><br>
               {main_otp} is your activation code.<br><br>
               Your registered email is {user_email}.<br><br>
               Your password is {user_password}<br><br>

               <span style="color:red">Remember, never share your password with anyone.</span><br><br>

               Kind Regards,<br>
               <b>The Cryptocurrency Investorsllc Team.</b>
              </p>
              
              
            </td>
          </tr>
        </tbody>
      </table>
    </center>
  </body>
</html>
"""
            
    
    recipient_list = [to,]    
    sender = 'Cryptocurrencyinvestorsllc noreply@cryptocurrencyinvestorsllc.com'



    def send_email(subject, message, html_message=None, sender=sender, recipent=recipient_list, image_path=None, image_name=None ):
        email = EmailMultiAlternatives(subject=subject, body=message, from_email=sender, to=recipient_list)
        if all([html_message, image_path, image_name]):
            email.attach_alternative(html_message, "text/html")
            email.content_subtype = 'html'
            email.mixed_subtype = 'related'


            image_path = "static/cryptocurrencyinvestorsllc/assets/img/ban-white.png"
            

            with open(image_path, 'r') as f:
                image = MIMEImage(f.read())
                image.add_header('Content-ID', '<{name}>'.format(name='ban-white.png'))
                image.add_header('Content-Disposition', 'inline', filename='ban-white.png')
                email.attach(image)
                image.add_header('Content-ID', f"<{image_name}>")
        email.send()

   # send_mail( subject, message=message, html_message=html_message,from_email=sender, recipient_list=recipient_list)
    
    email = EmailMultiAlternatives(subject=subject, body=message, from_email=sender, to=recipient_list)
    if all([html_message, image_path, image_name]):
        email.attach_alternative(html_message, "text/html")
        email.content_subtype = 'html'
        email.mixed_subtype = 'related'


        

        with open(image_path, 'rb') as f:
            image = MIMEImage(f.read())
            image.add_header('Content-ID', '<{name}>'.format(name=image_name))
            image.add_header('Content-Disposition', 'inline', filename=image_name)
            email.attach(image)
            image.add_header('Content-ID', f"<{image_name}>")
    email.send()   
    

    return render(request, 'account/send_otp.html')



@login_required(login_url='login')
def send_upgrade_email(request):
    
    

    user_email = request.user.email
    

    
    to = user_email
    subject = 'Account Placed On Hold'
    
    message = render_to_string('account/upgrade_email.html')
       
    
    recipient_list = [to,]    
    send_mail( subject, message, 'Cryptocurrencyinvestorsllc noreply@cryptocurrencyinvestorsllc.com', recipient_list ) 
 
    
    
   
    return render(request, 'account/send_upgrade_email.html')

@login_required(login_url='login')
def change_email_address(request):

    
    if request.POST:
        
        form = EmailAddressChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            email  = form.cleaned_data.get('email')

            user.email = email
            user.save()
            messages.success(request, "Hi {} Your Email Address was changed successsfully".format(request.user.first_name))
            return redirect('send_otp')
    else:
        form = EmailAddressChangeForm()

    context = {
            'form': form
        }
            


    return render(request, 'account/change_email_address.html', context)


@login_required(login_url='login')
def validate_phone_otp(request):
    
    
    if request.POST:
        
      

        otp_o1 = request.POST['digit-1']
        otp_o2 = request.POST['digit-2']
        otp_o3 = request.POST['digit-3']
        otp_o4 = request.POST['digit-4']
        otp_o5 = request.POST['digit-5']
        otp_o6 = request.POST['digit-6']

        otp_all = otp_o1 + otp_o2 + otp_o3 + otp_o4 + otp_o5 + otp_o6
        user_otp = otp_all
        
        if user_otp == main_otp:
            
            user = request.user
            if user.email_not_verified == True:
                user.email_not_verified = False
                user.save()

            
            
            messages.success(request, "Welcome {} Your account OTP was verified successsfully".format(request.user.first_name))
            return redirect('identity_verification_proceed')
        else:
            messages.info(request, "Invalid OTP ")
            return redirect('validate_otp')
    return render (request, 'account/validate_otp.html', )



@login_required(login_url='login')
def identity_verification(request):

    if request.user.email_not_verified:
        return redirect('send_otp')

    if request.user.is_admin:
        return redirect('home_page')

    
    
    if not request.user.email_not_verified:
        if request.user.id_card_verified:
            return redirect('user_dashboard')
            

    
    if request.POST:
        
        form = UserIDCardUploadForm(request.POST, request.FILES)
        if form.is_valid():
            
            form.save()
            return redirect('identity_verification_complete')
    else:
        form = UserIDCardUploadForm()

    
    context ={
        'form': form,
    }
   
    
    
    
    return render (request, 'account/identity_verification.html', context )




@login_required(login_url='login')
def identity_verification_proceed(request):

    if request.user.email_not_verified:
        return redirect('send_otp')

    if request.user.is_admin:
        return redirect('home_page')
    
    
    
    
    
    return render (request, 'account/identity_verification_proceed.html' )



@login_required(login_url='login')
def identity_verification_complete(request):

    if request.user.email_not_verified:
        return redirect('send_otp')

    if request.user.is_admin:
        return redirect('home_page')
    
    
    
    return render (request, 'account/identity_verification_complete.html' )

