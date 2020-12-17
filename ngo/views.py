from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from vauth.models import Applicant
from django.db.models import Q
from django.core.paginator import Paginator
import datetime
import requests
from django.contrib import messages
from .forms import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from vauth.mixins import ObjectViewMixin, visitor
from django.core.mail.message import make_msgid
WEBSITE_EMAIL = settings.WEBSITE_EMAIL

# Create your views here.
def is_valid(param):
    return param != '' and param is not None

def all_valid(params):
    count = 0
    for x in params:
        if is_valid(x):
            count += 1
    print(count, len(params))
    return count == len(params)

def recent_news():
    return Post.objects.select_related('category').all()[:3]


# @visitor
def index(request):
    return render(request, 'ngo/index.html', {'posts':recent_news()})

# @visitor   
def about(request):
    return render(request, 'ngo/about.html')

# @visitor
def contact(request):
    form = ContactForm()
    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            context = {
                'name' : form.cleaned_data['name'],
                'email' : form.cleaned_data['email'],
                'phone' : form.cleaned_data['phone'],
                'message' : form.cleaned_data['message'],
            }
            content = render_to_string('emails/contact.html', context)
            email = EmailMessage(
                'Contact',
                content,
                context['email'],
                [WEBSITE_EMAIL,],
                headers={'Message-ID': make_msgid()},
            )
            email.content_subtype = "html"
            email.send()
            messages.success(request, "An Email has been sent to the respective personnel, you will be reached out to soon")
        else:
            messages.error(request, "Please fill all required fields", "danger")
            
    return render(request, 'ngo/contact.html')

# @visitor
def events(request):
    date = request.GET.get('date')
    location = request.GET.get('location')
    tag = request.GET.get('tag')
    term = request.GET.get('search')
    event_list = Event.objects.all()
    if is_valid(location):
        event_list = event_list.filter(location__icontains=location)
    if is_valid(tag):
        event_list = event_list.filter(tags__name__in=[tag])
    if is_valid(date):
        event_list = event_list.filter(due_datetime__date__lte=date)
    if is_valid(term):
        event_list = event_list.filter(title__icontains=term)
    paginator = Paginator(event_list, 1)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    context = {'events':events, 'next_10':events.number +10, 'previous_5':events.number -5}
    if all_valid([date,location,tag]) > 0:
        context['search'] = True
        if is_valid(date):
            day = date.split('-')
            context['date'] = datetime.date(int(day[0]), int(day[1]), int(day[2]))
            context['raw_date'] = date
        if is_valid(location):
            context['location'] = location
        if is_valid(tag):
            context['tag'] = tag
    return render(request, 'ngo/events.html', context)

# @visitor
def event_details(request, slug):
    event = get_object_or_404(Event, slug=slug)
    categories = Category.objects.filter(cat_type="P")
    context = {'cobject':event, 'event':True, 'news':recent_news(), 'categories':categories}
    return render(request, 'ngo/details.html', context)

# @visitor
def blog(request):
    term = request.GET.get('search')
    tag = request.GET.get('tag')
    catslug = request.GET.get('category')
    categories = Category.objects.filter(cat_type="P")
    catqs = categories.filter(slug=catslug)
    post_list = Post.objects.select_related('author').all()
    if is_valid(term):
        post_list = post_list.filter(title__icontains=term)
    if is_valid(tag):
        post_list = post_list.filter(tags__name__in=[tag])
    if is_valid(catslug) and catqs.exists():
        post_list = post_list.filter(category=catqs[0])
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {'posts':posts, 'categories':categories, 'next_10':posts.number +10, 'previous_5':posts.number -5}
    context['news'] = post_list[:3]
    if is_valid(term):
        context['term'] = term
    if is_valid(tag):
        context['tag'] = tag
    if is_valid(catslug) and catqs.exists():
        context['category'] = catqs[0]
    return render(request, 'ngo/blog.html', context)

# @visitor
def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    categories = Category.objects.filter(cat_type="P")
    context = {'cobject':post, 'post':True, 'news':recent_news(), 'categories':categories}
    return render(request, 'ngo/details.html', context)

# @visitor
def projects(request):
    categories = Category.objects.filter(cat_type="PR")
    projects = Project.objects.all()
    context = {'projects':projects, 'categories':categories}
    return render(request, 'ngo/projects.html', context)

# @visitor
def project_details(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {'cobject':project, 'project':True, 'news':recent_news()}
    return render(request, 'ngo/details.html', context)

# @visitor
def search(request):
    term = request.GET.get('search')
    context = {}
    qe = Event.objects.filter(title__icontains=term)
    if qe.exists():
        events = qe[:5]
        context['events'] = events
    qp = Post.objects.filter(title__icontains=term)
    if qp.exists():
        posts = qp[:5]
        context['posts'] = posts
    context['term'] = term
    return render(request, 'ngo/search.html', context)

# scrollspy
# @visitor
def category(request, option, cat):
    if option == "Posts":
        category = Category.objects.filter(cat_type="P", title=cat)
        template = "ngo/blog.html"
    elif option == "Projects":
        category = Category.objects.filter(cat_type="PR", title=cat)
        template = "ngo/projects.html"
    return render (request, template, {'category':category})

# @visitor
def gallery(request):
    image_list = Image.objects.all()
    paginator = Paginator(image_list, 2)
    page_number = request.GET.get('page')
    images = paginator.get_page(page_number)
    context = {'images':images, 'news':recent_news()}
    return render(request, 'ngo/gallery.html', context)

# @visitor
def join(request):
    form = ApplicantForm()
    if request.POST:
        form = ApplicantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Applied, we'll be in touch!!")
        else:
            messages.error(request, "Please fill all fields appropriately!!!", extra_tags="danger")
    return render(request, "ngo/join.html", {"form":form})

# @visitor
def subscribe(request):
    if request.POST:
        form = SubscriberForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['email'])
            if user.exists():
                if user.profile.subscribed:
                    messages.error(request,"A user has used this email already!!", extra_tags="danger")
                else:
                    user.profile.subscribed = True
            else:
                form.save()
            messages.success(request,"Thank you for subscribing to our newsletter")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request,"Someone has used this email already!!", extra_tags="danger")
            return redirect(request.META['HTTP_REFERER'])

# @visitor
def unsubscribe(request, email):
    sub = Subscriber.objects.filter(email=email)
    user = User.objects.filter(email=email)
    if sub.exists():
        sub[0].delete()
    elif user.exists():
        user[0].profile.subscribed=False
        user[0].save()
    return HttpResponse("<h1>Successfuly Unsubscribed</h1>")