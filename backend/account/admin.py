from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from .models import User,Server,Error
from django.contrib.auth.models import  Group

from unfold.admin import ModelAdmin
from django import forms
from django.contrib import admin


class UserPasswordAdminForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        label="Password",
        widget=forms.TextInput(attrs={'type':'password'}),
        help_text="Enter a new password (leave blank to keep the current password)."
    )

    class Meta:
        model = Server
        fields = ['username', 'password','ip']
        

    def save(self, commit=True):
        """
        Hash the password if a new one is provided.
        """
        instance = super().save(commit=False)
        raw_password = self.cleaned_data.get('password')
        if raw_password:
            instance.password = raw_password
        if commit:
            instance.save()
        return instance

# admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass



class ServerAdmin(ModelAdmin):
    form = UserPasswordAdminForm
    list_display = ('username','id',"ip",  )  # Fields to display in the admin list view
    search_fields = ('ip','username')  # Allow searching by description

    
admin.site.register(Server, ServerAdmin)



class ErrorAdmin(ModelAdmin):
    list_display = ('id',"created_at",  )  # Fields to display in the admin list view
    
admin.site.register(Error, ErrorAdmin)

