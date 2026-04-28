from django import forms


class PasswordChangeForm(forms.Form):

    new_password = forms.CharField(
        widget=forms.PasswordInput()
    )

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()