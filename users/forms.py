from django.contrib.auth.forms import (
    UserCreationForm as DefaultUserCreationForm, 
    UserChangeForm as DefaultUserChangeForm
)
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreationForm(DefaultUserCreationForm):
    class Meta:
        model = User
        fields = ('email',)
    
class UserChangeForm(DefaultUserChangeForm):
    class Meta:
        model = User
        fields = ('email',)