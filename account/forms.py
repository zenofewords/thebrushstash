from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
)

from account.models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email address already exits.')
        return email


class AddressForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'email', 'country', 'city', 'state_county', 'zip_code',
            'note', 'company_name', 'company_address', 'company_uin',
        )


class CustomUserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': 'The two password fields didn\'t match.',
    }
    email = forms.EmailField(max_length=200, help_text='Required')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput,
                                help_text='Enter the same password as above, for verification.')

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email address already exits.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class ChangeForm(UserChangeForm):
    password = auth_forms.ReadOnlyPasswordHashField(
        label='Password',
        help_text='''Raw passwords are not stored, so there is no way to see
                  this user's password, but you can change the password
                  using <a href=\'../password/\'>this form</a>''')

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_password(self):
        return self.initial['password']
