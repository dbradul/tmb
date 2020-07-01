from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from account.models import User


class AccountRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.all().filter(email=email).exists():
            raise ValidationError('Email already exists')

        return email



class AccountProfileForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image')

    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.all()\
                .filter(email=email)\
                .exclude(id=self.instance.id)\
                .exists():
            raise ValidationError('Email already exists')

        return email


#
# class UserProfileUpdateForm(ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['image']


# class UserAccountProfileForm(ModelForm):
#
#     class Meta:
#         model = UserProfile
#
#         fields = '__all__'
#
#     def clean_email(self):
#
#         email = self.cleaned_data['email']
#
#         if User.objects.all().filter(email=email).exclude(id=self.instance.id).exists():
#             raise ValidationError('Email already exists')
#
#         return email
#
#     def clean(self):
#         return super().clean()
#
#
#     def save(self, commit=True):
#         return super().save(commit)


#
# class UserAccountProfileForm2(ModelForm):
#
#     class Meta:
#         model = UserProfile
#         exclude = ()
#
#
# UserAccountProfileFormSet = inlineformset_factory(
#     User, UserProfile, form=UserAccountProfileForm2,
#     fields=['image'], can_delete=False
#     )
