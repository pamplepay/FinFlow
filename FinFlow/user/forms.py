from .models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password

class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].widget.attrs.update({     
            'class': 'form-control',
            'autofocus': False
        })

        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })
        
        self.fields['user_biznum'].label = '사업자번호'
        self.fields['user_biznum'].widget.attrs.update({     
            'class': 'form-control',
            'autofocus': False
        })

        self.fields['hp'].label = '휴대폰번호'
        self.fields['hp'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['auth'].label = '인증번호'
        self.fields['auth'].widget.attrs.update({
            'class': 'form-control',
        })

    class Meta:
        model = User
        fields = ['user_id', 'password1', 'password2', 'user_biznum', 'hp', 'auth',]

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.level = '2'
        user.save()

        return user

class LoginForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control',}), 
        max_length=16,
        label='아이디'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
        attrs={'class': 'form-control',}),
        label='비밀번호'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')

        if user_id and password:
            try:
               user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                self.add_error('user_id', '아이디가 존재하지 않습니다.')
                return
            
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')