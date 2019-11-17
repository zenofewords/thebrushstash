from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.safestring import mark_safe

from account.models import CustomUser


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = CustomUser
        fields = ('email', )

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email address already exits.')
        return email


class PasswordForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': 'The two password fields didn\'t match.',
    }
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password'}
        )
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Repeat password'}
        ),
        help_text='Enter the same password as above, for verification.'
    )

    class Meta:
        model = CustomUser
        fields = ('password1', 'password2', )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


class AddressForm(forms.ModelForm):
    note = forms.CharField(
        label='note',
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Note (optional)'})
    )
    register = forms.BooleanField()
    subscribe_to_newsletter = forms.BooleanField()
    agree_to_terms = forms.BooleanField()
    r1_receipt = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].empty_label = 'Select country'
        self.fields['country'].required = True

        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'

        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'

        self.fields['email'].required = True
        self.fields['email'].widget.attrs['placeholder'] = 'Email address'

        self.fields['phone_number'].required = False
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone number'

        self.fields['address'].required = True
        self.fields['address'].widget.attrs['placeholder'] = 'Address'

        self.fields['city'].required = True
        self.fields['city'].widget.attrs['placeholder'] = 'City'

        self.fields['zip_code'].required = True
        self.fields['zip_code'].widget.attrs['placeholder'] = 'Postcode/ZIP'

        self.fields['state_county'].required = False
        self.fields['state_county'].widget.attrs['placeholder'] = 'State/County (optional)'

        self.fields['register'].label = 'Create an account'
        self.fields['register'].label_suffix = ''
        self.fields['register'].initial = True
        self.fields['register'].required = False

        self.fields['subscribe_to_newsletter'].label = 'Subscribe to our newsletter'
        self.fields['subscribe_to_newsletter'].label_suffix = ''
        self.fields['subscribe_to_newsletter'].initial = True
        self.fields['subscribe_to_newsletter'].required = False

        self.fields['r1_receipt'].label = 'I need an R1 receipt'
        self.fields['r1_receipt'].label_suffix = ''
        self.fields['r1_receipt'].initial = False
        self.fields['r1_receipt'].required = False

        self.fields['agree_to_terms'].label = mark_safe(
            '''I have read and agree to the <a href="/general-terms-and-conditions/"
            target="_blank" rel="noopener noreferrer">terms and conditions</a>'''
        )
        self.fields['agree_to_terms'].label_suffix = ''
        self.fields['agree_to_terms'].initial = False
        self.fields['agree_to_terms'].error_messages = {
            'required': 'We need you to agree to the terms and conditions to continue.'
        }

    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'email', 'phone_number', 'country', 'address', 'city',
            'state_county', 'zip_code', 'company_name', 'company_address', 'company_uin',
            'note', 'register', 'subscribe_to_newsletter', 'agree_to_terms',
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
        user = super().save(commit=False)
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
