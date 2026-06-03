from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tên đăng nhập',
            'id': 'id_username',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mật khẩu',
            'id': 'id_password',
            'autocomplete': 'current-password',
        })
    )
    remember_me = forms.BooleanField(required=False, initial=False)

from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'receive_call_alerts']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'VD: +84987654321'}),
            'receive_call_alerts': forms.CheckboxInput(attrs={'class': 'toggle-checkbox'}),
        }
