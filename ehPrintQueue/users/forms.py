from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        username = forms.CharField(label="Username", max_length=30,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
        password = forms.CharField(label="Password", max_length=30,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'password'}))


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control'}), label='Username')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
                                label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password Again',
                                                                  'class': 'form-control'}),
                                label='Retype Password')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
                                 label='First Name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
                                label='Last Name')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@example.com',
                                                            'class': 'form-control'}), label='Email Address')
    isAdmin = forms.BooleanField(label='Administrator', required=False)

    isCC = forms.BooleanField(label='Administrator', required=False)


    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(message='Username: ' + username + 'taken. Please select a different username.')

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("The passwords do not match")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']


class editProfile(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@example.com',
                                                            'class': 'form-control'}), label='Email Address')
    class Meta:
        model = User
        fields = ['email']