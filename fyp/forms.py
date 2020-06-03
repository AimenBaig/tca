from django import forms
from fyp.models import tbl_messages, tbl_users, tbl_user_role, tbl_api_setting, tbl_system_setting


class MessageForm(forms.ModelForm):
    class Meta:
        model = tbl_messages
        fields = ("msg_subject", "message")
        widgets = {
            'msg_subject': forms.TextInput(
                attrs={
                    'placeholder': 'Subject',
                    'class': 'form-control form-control-user',
                    'required': True
                }
            ),
            'message': forms.TextInput(
                attrs={
                    'placeholder': 'Mail Body',
                    'class': 'form-control',
                    'required': True
                }
            )
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = tbl_users
        fields = ("email", "password")
        widgets = {
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Email Address',
                    'class': 'form-control form-control-user',
                    'required': True
                }
            ),
            'password': forms.TextInput(
                attrs={
                    'placeholder': 'Password',
                    'class': 'form-control form-control-user',
                    'required': True,
                    'type': 'password'
                }
            )
        }


class AddRoleForm(forms.ModelForm):
    class Meta:
        model = tbl_user_role
        fields = "__all__"
        widgets = {
            'role': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Title of Role',
                    'class': 'form-control form-control-user',
                    'required': True
                }
            )
        }


class AddUsers(forms.ModelForm):
    class Meta:
        model = tbl_users
        fields = "__all__"
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'First Name',
                    'class': 'form-control form-control-user',
                    'required': True
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Last Name',
                    'class': 'form-control form-control-user',
                    'required': True
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'User Email',
                    'class': 'form-control form-control-user',
                    'required': True,
                    'type': 'email'
                }
            ),
            'password': forms.TextInput(
                attrs={
                    'placeholder': 'Password',
                    'class': 'form-control form-control-user',
                    'required': True,
                    'type': 'password'
                }
            ),
            'phone_no': forms.TextInput(
                attrs={
                    'placeholder': 'Phone No',
                    'class': 'form-control form-control-user',
                    'required': False,
                }
            ),
            'photo': forms.TextInput(
                attrs={
                    'placeholder': 'Upload Photo',
                    'class': 'form-control',
                    'required': False,
                    'type': 'file'
                }
            ),
            'HQ_id': forms.TextInput(
                attrs={
                    'placeholder': 'Upload Photo',
                    'class': 'form-control form-control-user',
                    'required': False,
                }
            ),
            'role_id': forms.TextInput(
                attrs={
                    'placeholder': 'Upload Photo',
                    'class': 'form-control form-control-user',
                    'required': False,
                }
            ),
            'designation_id': forms.TextInput(
                attrs={
                    'placeholder': 'Upload Photo',
                    'class': 'form-control form-control-user',
                    'required': False,
                }
            ),

        }


class APIForm(forms.ModelForm):
    class Meta:
        model = tbl_api_setting
        fields = "__all__"
        widgets = {
            'api_key': forms.TextInput(
                attrs={
                    'placeholder': 'API Key',
                    'class': 'form-control form-control-user',
                    'required': True
                }
            ),
            'api_key_secret': forms.TextInput(
                attrs={
                    'placeholder': 'API Secret Key',
                    'class': 'form-control form-control-user',
                    'required': True
                }
            ),
            'access_token': forms.TextInput(
                attrs={
                    'placeholder': 'Access Token',
                    'class': 'form-control form-control-user',
                    'required': True
                }
            ),
            'access_token_secret': forms.TextInput(
                attrs={
                    'placeholder': 'Access Secret',
                    'class': 'form-control form-control-user',
                    'required': True
                }
            ),
        }


class SystemSettingForm(forms.ModelForm):
    class Meta:
        model = tbl_system_setting
        fields = "__all__"
        widgets = {
            'system_name': forms.TextInput(
                attrs={
                    'placeholder': 'System Name',
                    'class': 'form-control form-control-user',
                    'required': True
                }
            ),
        }
