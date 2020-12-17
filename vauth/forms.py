from django import forms
from .validators import validate_file_extension
from django.contrib.auth.models import User
from django.forms import ModelForm
from ngo.views import Post
from ckeditor.widgets import CKEditorWidget

class ProfileForm(ModelForm):
    location = forms.CharField(required=False)
    about = forms.CharField(required=False, widget=forms.Textarea())
    phone_number = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    def save(self, commit=True):
        user = self.instance
        user.profile.location = self.cleaned_data['location']
        user.profile.about = self.cleaned_data['about']
        user.profile.phone_number = self.cleaned_data['phone_number']
        user.profile.save()
        if commit:
            return super(ProfileForm, self).save()



    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get("username")
    #     users = User.objects.all()
    #     if username and subject and "help" not in subject:
    #         msg = "Must put 'help' in subject when cc'ing yourself."
    #         self.add_error('username', msg)
    #         self.add_error('subject', msg)
    
class PostForm(ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    cover = forms.ImageField(validators=[validate_file_extension], required=False)
    class Meta:
        model = Post
        # fields = [ 'title', 'tags', 'quote', 'content', 'cover', 'category']
        exclude = ['created', 'slug', 'author']

class NewsletterForm(forms.Form):
    title = forms.CharField()
    body = forms.CharField(widget=CKEditorWidget())

class PictureForm(forms.Form):
    picture = forms.ImageField(validators=[validate_file_extension])

class LoginForm(forms.Form):
    username= forms.CharField()
    password = forms.CharField(widget=(forms.PasswordInput()))
    remember = forms.CharField(widget=(forms.CheckboxInput))