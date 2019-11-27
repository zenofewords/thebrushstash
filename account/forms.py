from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from account.models import CustomUser
from thebrushstash.constants import (
    form_mandatory_fields,
    form_extra_fields,
)


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, help_text=_('Required'))

    class Meta:
        model = CustomUser
        fields = ('email', )

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_('An account with this e-mail address already exits.'))
        return email


class PasswordForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn\'t match.'),
    }
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={'placeholder': _('Password')}
        )
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(
            attrs={'placeholder': _('Repeat password')}
        ),
        help_text=_('Enter the same password as above, for verification.')
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
        widget=forms.Textarea(attrs={'placeholder': _('Note (optional)')})
    )
    register = forms.BooleanField()
    subscribe_to_newsletter = forms.BooleanField()
    agree_to_terms = forms.BooleanField()
    r1_receipt = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].empty_label = _('Select country')
        self.fields['country'].required = True
        self.fields['country'].to_field_name = 'name'

        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs['placeholder'] = _('First name')

        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs['placeholder'] = _('Last name')

        self.fields['email'].required = True
        self.fields['email'].widget.attrs['placeholder'] = _('E-mail address')

        self.fields['phone_number'].required = False
        self.fields['phone_number'].widget.attrs['placeholder'] = _('Phone number')

        self.fields['address'].required = True
        self.fields['address'].widget.attrs['placeholder'] = _('Address')

        self.fields['city'].required = True
        self.fields['city'].widget.attrs['placeholder'] = _('City')

        self.fields['zip_code'].required = True
        self.fields['zip_code'].widget.attrs['placeholder'] = _('Postcode/ZIP')

        self.fields['state_county'].required = False
        self.fields['state_county'].widget.attrs['placeholder'] = _('State/County (optional)')

        self.fields['company_name'].required = False
        self.fields['company_name'].widget.attrs['placeholder'] = _('Company name')

        self.fields['company_address'].required = False
        self.fields['company_address'].widget.attrs['placeholder'] = _('Company address')

        self.fields['company_uin'].required = False
        self.fields['company_uin'].widget.attrs['placeholder'] = _('Company UIN')

        self.fields['register'].label = _('Create an account')
        self.fields['register'].label_suffix = ''
        self.fields['register'].initial = True
        self.fields['register'].required = False

        self.fields['subscribe_to_newsletter'].label = _('Join to get the latest news from TBS')
        self.fields['subscribe_to_newsletter'].label_suffix = ''
        self.fields['subscribe_to_newsletter'].initial = True
        self.fields['subscribe_to_newsletter'].required = False

        self.fields['r1_receipt'].label = _('I need an R1 receipt')
        self.fields['r1_receipt'].label_suffix = ''
        self.fields['r1_receipt'].initial = False
        self.fields['r1_receipt'].required = False

        self.fields['agree_to_terms'].label = mark_safe(
            _('''I have read and agree to the <a href="/general-terms-and-conditions/"
            target="_blank" rel="noopener noreferrer">terms and conditions</a>''')
        )
        self.fields['agree_to_terms'].label_suffix = ''
        self.fields['agree_to_terms'].initial = False
        self.fields['agree_to_terms'].error_messages = {
            'required': _('You must agree to the terms and conditions to continue.')
        }

    class Meta:
        model = CustomUser
        fields = form_mandatory_fields + form_extra_fields


class CustomUserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn\'t match.'),
    }
    email = forms.EmailField(max_length=200, help_text=_('Required'))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput,
                                help_text=_('Enter the same password as above, for verification.'))

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_('An account with this e-mail address already exits.'))
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
        label=_('Password'),
        help_text='''Raw passwords are not stored, so there is no way to see
                  this user's password, but you can change the password
                  using <a href=\'../password/\'>this form</a>''')

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_password(self):
        return self.initial['password']
