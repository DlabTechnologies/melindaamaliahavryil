from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User, UserWithdrawRequest, ManagerWalletAddress,NewsletterSignup, UserDepositRequest, Account_level, ManagerContactInfo, ContactForm, RecentPayouts, User_ID_Card_Upload
from .forms import UserChangeForm, UserCreationForm

class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    

   

    






class ManagerContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email','phone')

class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone','subject','message','time')





admin.site.register(ManagerContactInfo, ManagerContactInfoAdmin)
admin.site.register(ContactForm, ContactFormAdmin)
 
    