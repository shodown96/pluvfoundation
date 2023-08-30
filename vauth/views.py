from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages
from ngo.models import *
from ngo.views import is_valid
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login
from payment.models import Payment
import datetime
###########################
from django.contrib.auth import login
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
import os
import logging
logger = logging.getLogger(__name__)
from django.core.mail.message import make_msgid
from django.db.models import Sum
from django.http import JsonResponse
import json
from ngo.views import is_valid
# Create your views here.
WEBSITE_EMAIL = settings.WEBSITE_EMAIL

def get_subscribers():
    emails = []
    users = Profile.objects.filter(subscribed=True)
    subscribers = Subscriber.objects.all()
    for x in users:
        emails.append(x.user.email)
    for y in subscribers:
        emails.append(y.email)
    return emails

def mylogin(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username,password=password)
            if user:
                login(request,user)
                remember = form.cleaned_data['remember']
                print(remember)
                if remember != True:
                    request.session.set_expiry(0)
                    print("expiring")
                messages.success(request,"Welcome back "+user.first_name)
                if is_valid(request.GET.get("next")):
                    return redirect(request.GET.get("next"))
                return redirect("vauth:profile")
            else:
                form.add_error(None,error="Invalid Credentials")

                return render(request, "registration/login.html", {'form':form})
        else:
            form.add_error(None,error="Please fill all fields appropriately")
            return render(request, "registration/login.html", {'form':form})


@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)[:3]
    return render(request, 'vauth/dashboard.html', {'posts':posts})

@login_required
def profile(request):
    form = ProfileForm()
    if request.POST:
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            error = dict(form.errors)
            messages.error(request, error, extra_tags="danger")
    return render(request, 'vauth/profile.html', {'form':form})

@login_required
def dp(request):
    form = PictureForm()
    if request.POST and request.FILES:
        form = PictureForm(data=request.FILES, files=request.FILES)
        if form.is_valid():
            if request.user.profile.dp:
               request.user.profile.dp.delete()
            content = form.cleaned_data['picture']
            ext = os.path.splitext(content.name)[1]
            name = request.user.username + "-dp"+ext
            request.user.profile.dp.save(name,content)
            request.user.profile.save()
        else:
            error = dict(form.errors)
            messages.error(request, error['picture'], extra_tags="danger")
        # picture = request.FILES.get('')
    return render(request, 'vauth/profile.html', {'form':form})


@login_required
def posts(request):
    form = PostForm()
    categories = Category.objects.filter(cat_type="P")
    post_list = Post.objects.select_related('author').filter(author=request.user)
    paginator = Paginator(post_list,6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    if request.POST:
        if request.FILES:
            form = PostForm(data=request.POST, files=request.FILES)
            if form.is_valid() and form.is_multipart():
                title = form.cleaned_data['title']
                cover = form.cleaned_data['cover']
                new_post = form.save(commit=False)
                # print(cover.name)
                new_post.author = request.user
                new_post.slug = "".join(title).replace(' ', '-').lower()
                new_post.cover.save(name=new_post.slug+cover.name[-4:], content=cover)
                # new_post.slug.replace(' ', '-').lower().strip("('')"),
                new_post.save()
                form.save_m2m()
                messages.success(request, "New Post Published")
            else:
                messages.error(request, "Please fill all required fields", extra_tags="danger")
        else:
            messages.error(request, "Please fill all required fields", extra_tags="danger")
            logger.error(form.errors.as_text())
    context = {'form':form, 'categories':categories, 'posts':posts, 'next_10':posts.number +10, 'previous_5':posts.number -5}
    return render(request, 'vauth/posts.html', context )


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    form = PostForm(instance=post)
    if post.author_id == request.user.id:
        if request.POST:
            form = PostForm(data=request.POST, files=request.FILES or None, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.slug = "".join(post.title).replace(' ', '-').lower()
                if request.FILES.get('cover'):
                    cover = form.cleaned_data['cover']
                    post.cover.save(name=post.slug+cover.name[-4:], content=cover)
                    print(cover.name)
                post.save()
                form.save_m2m()
                messages.success(request, "Post Edited")
            else:
                messages.error(request, "Please fill all required fields", extra_tags="danger")
    else:
        messages.error(request, "You didn't create this Post", extra_tags="danger")
    return render(request, "vauth/post.html", {'form':form, 'post':post})



@login_required
def tasks(request):
    return render(request, 'vauth/tasks.html')

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = True
    task.save()
    return redirect("vauth:tasks")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError,OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.verified = True
        user.save()
        login(request, user)
        messages.success(request, "Your Account has been verified, Thank you for joining Us")
        return redirect('login')
    else:
        return HttpResponse("<h1 style='text-align:center'>Token Expired</h1>")


@login_required
def newsletter(request):
    if request.user.is_superuser:
        form = NewsletterForm()
        if request.POST:
            form = NewsletterForm(request.POST)
            if form.is_valid():
                for email in get_subscribers():
                    current_site = get_current_site(request)
                    title = form.cleaned_data['title']
                    body = form.cleaned_data['body']
                    content = render_to_string('emails/newsletter.html',
                    {'title':title, 'body':body, 'domain':current_site.domain, "email":email}
                        )
                    email = EmailMessage(
                    "PLUV Foundation Newsletter",
                    content,
                    WEBSITE_EMAIL,
                    [email,],
                    headers={'Message-ID': make_msgid()},
                    )
                    email.content_subtype = "html"
                    email.send()
                    messages.success(request, "Newsletter Sent To all Subscribers")
            else:
                messages.error(request, "Please fill all required fields", extra_tags="danger" )
        context = {'form':form}
        return render(request, 'vauth/newsletter.html', context)
    else:
        messages.error(request, "Sorry but you're not authorized to do this", extra_tags="danger" )

@login_required
def analytics(request):
    if request.user.is_superuser:
        # visitors = Visitor.objects.all()
        active_users = User.objects.filter(is_active=True)
        inactive_users = User.objects.filter(is_active=False)
        today = datetime.datetime.today()
        logged_in_users = User.objects.filter(last_login__day=today.day)
        donations = Payment.objects.filter(paid=True)
        subscribers = Subscriber.objects.all().count() + Profile.objects.filter(subscribed=True).count()
        total_amount = donations.aggregate(Sum("amount"))["amount__sum"]
        data = {
            'visitors': [],
            'donations': []
        }
        chart_donations = donations.filter(paid_at__year=today.year)
        # chart_visitors = visitors.filter(timestamp__year=today.year)
        for x in range(1,13):
            pays = chart_donations.filter(paid_at__month=x)
            # vis = chart_visitors.filter(timestamp__month=x)
            # print("pays "+str(x),pays.aggregate(Sum("amount"))["amount__sum"])
            if pays.exists():
                data['donations'].append(pays.aggregate(Sum("amount"))["amount__sum"])
            else:
                data['donations'].append(0)
            # if vis.exists():
            #     data['visitors'].append(vis.count())
            # else:
            #     data['visitors'].append(0)

        context = {
            # 'visitors':visitors,
            'active_users':active_users,
            'inactive_users':inactive_users,
            'logged_in_users':logged_in_users,
            'donations':donations,
            'total_amount':total_amount,
            'subscribers':subscribers,
            'posts': Post.objects.all(),
            'events':Event.objects.all(),
            'chart_donations':data['donations'],
            'chart_visitors': data['visitors'],
            'year': today.year
        }
        return render(request, "vauth/analytics.html", context)
    else:
        messages.error(request, "You're not the admin, this page isn't meant for you", "danger")
        return redirect("ngo:index")


def ajax_donations(request):
    data = { 'amounts': [] }
    if request.is_ajax() and request.GET:
        year = request.GET.get("year")
        if is_valid(year):
            donations = Payment.objects.filter(paid=True, paid_at__year=int(year))
            for x in range(1,13):
                pays = donations.filter(paid_at__month=x)
                if pays.exists():
                    data['amounts'].append(pays.aggregate(Sum("amount"))["amount__sum"])
                else:
                    data['amounts'].append(0)
    return JsonResponse(data=data)
            

def ajax_visitors(request):
    data = { 'visitors': [] }
    # if request.is_ajax() and request.GET:
    #     year = request.GET.get("year")
    #     if is_valid(year):
    #         visitors = Visitor.objects.filter(timestamp__year=int(year))
    #         for x in range(1,13):
    #             vis = visitors.filter(timestamp__month=x)
    #             if vis.exists():
    #                 data['visitors'].append(vis.count())
    #             else:
    #                 data['visitors'].append(0)
    return JsonResponse(data=data)

  