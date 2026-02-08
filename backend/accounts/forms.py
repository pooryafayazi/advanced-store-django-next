# backend\accounts\forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "is_active", "is_staff", "is_verified", "type")

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password (hashed)")

    class Meta:
        model = User
        fields = ("email", "password", "is_active", "is_staff", "is_verified", "type")

    def clean_password(self):
        return self.initial["password"]
