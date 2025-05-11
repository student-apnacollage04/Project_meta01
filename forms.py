from django import forms
from .models import userModel
from .models import quiry

class userForm(forms.ModelForm):
    class Meta:
        model = userModel
        fields = ['username','contact','email','password','cpassword']

class quiryForm(forms.ModelForm):
    class Meta:
        model = quiry
        fields = ['uname','umail','uquery']