from django import forms
from .models import User, Student, Teacher, Classroom, Document
from django.utils.translation import gettext_lazy
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())

class GoogleForm(forms.Form):
    CHOICES = [('student', 'Student'), ('teacher', 'Teacher')]
    username = forms.CharField(label='Username', max_length=150)
    type_of_user = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(GoogleForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['type_of_user'].required = True

    def clean_username(self):
        username = self.cleaned_data['username']
        if(User.objects.filter(username=username).exists()):
            self.add_error('username', 'Username already exists.')
        return username


class RegistrationForm(forms.ModelForm):
    CHOICES = [('student', 'Student'), ('teacher', 'Teacher')]
    type_of_user = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    repeat_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ['username', 'password', 'repeat_password', 'email', 'first_name', 'last_name', 'type_of_user']
        labels = {
            'repeat_password' : gettext_lazy('Repeat Password'),
        }
        widgets = {
            'password' : forms.PasswordInput()
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if(User.objects.filter(email=email).exists()):
            self.add_error('email', 'Email already exists.')
        return email


    # called after specific field cleaning
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeated_password = cleaned_data.get('repeat_password')

        if(password != repeated_password):
            self.add_error('password', 'Passwords do not match.')


class AddClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'start_date' : forms.SelectDateWidget(
                empty_label=("Choose Year", "Choose Month", "Choose Day"),
            ),
            'end_date' : forms.SelectDateWidget(
                empty_label=("Choose Year", "Choose Month", "Choose Day"),
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if(Classroom.objects.filter(name=name).exists()):
            self.add_error('name', 'Classroom with name already exists.')

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if(start_date >= end_date):
            self.add_error('end_date', 'End date must be greater than start date')

        return cleaned_data

class AddDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'document_file']

class StudentUploadPhotoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentUploadPhotoForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = True
    class Meta:
        model = Student
        fields = ['photo']
        labels = {
            'photo' : gettext_lazy('Upload new photo (make sure your face is visible)'),
        }
