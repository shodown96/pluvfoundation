from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
import random, string
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
import datetime
from django.conf import settings
address = settings.ADDRESS
# Register your models here.

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
WEBSITE_EMAIL = settings.WEBSITE_EMAIL

admin.AdminSite.site_header = "PLUV Foundation Administration"
admin.AdminSite.site_title = "PLUV Foundation Admin"

def make_user(modeladmin, request, queryset):
    count = 1
    for x in queryset:
        new_user = User(
            first_name=x.first_name,
            last_name=x.last_name,
            username=str(x.last_name+"."+x.first_name),
            email = x.email
        )
        password = User.objects.make_random_password(10)
        new_user.set_password(password)
        new_user.is_active = False
        new_user.save()
        new_user.profile.sex = x.sex
        new_user.profile.about = x.statement
        new_user.profile.location = x.address
        current_site = get_current_site(request)
        content = render_to_string('emails/new_user.html',
            {
                'fname':new_user.first_name,
                'username':new_user.username,
                'password':password,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
                'date': datetime.datetime.today(),
                'address':address
            })
        email = EmailMessage(
            'PLUV Membership',
            content,
            WEBSITE_EMAIL,
            [x.email],
            headers={'Message-ID': count},
        )
        email.content_subtype = "html"
        email.send()
        count += 1
        
    messages.success(request, str(queryset.count())+' Appliants have been made Users and emails have been sent')
make_user.short_description = "Make selected Users"

def delete_inactive_users(modeladmin, request, queryset):
    for x in queryset:
        if not x.is_active:
            x.delete
    messages.success(request, "Inactive users deleted")
delete_inactive_users.short_description = "Delete Inactive Users"

def verify_tasks(modeladmin, request, queryset):
    count = 0
    for x in queryset:
        if  not x.verified:
            count +=1
    queryset.update(verified=True)
    messages.success(request, str(count)+" Tasks verified")
verify_tasks.short_description = "Verify Tasks"

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'verified', 'dp', 'sex', 'date_joined']
    list_display_links = ['user','dp']

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'timestamp', 'completed', 'verified']
    actions = [verify_tasks]

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'middle_name', 'email', 'phone_number', 'date_applied']
    actions = [make_user]

class VisitorAdmin(admin.ModelAdmin):
    list_display = ['user','ip_address', 'timestamp']

UserAdmin.actions = [delete_inactive_users]
    
admin.site.register(Profile , ProfileAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Visitor, VisitorAdmin)