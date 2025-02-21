from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ClientData
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.

from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from account.models import User
from django.utils.html import format_html
import json
import random

from django.views.generic import TemplateView
from unfold.admin import ModelAdmin
from unfold.views import UnfoldModelAdminViewMixin
from django.urls import path

class MyClassBasedView(UnfoldModelAdminViewMixin, TemplateView):
    title = "plots"  # required: custom page header title
    permission_required = ()  # required: tuple of permissions
    template_name = "admin/charts.html"

    def get_context_data(self, **kwargs):
        # Get the default context
        context = super().get_context_data(**kwargs)
        # Add your custom context
        # context["custom_variable"] = "Custom Value"
        # context["another_variable"] = {"key": "value"}
        object_id = kwargs.get("id")
        WEEKDAYS = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun",
        ]

        positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
        average = [r[1] - random.randint(3, 5) for r in positive]
        performance_positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
        performance_negative = [
            [-1, -random.randrange(8, 28)] for i in range(1, 28)]

        context.update(
            {
                'user_chart' : ClientData.objects.get(id=object_id).author ,
                "kpi": [
                    {
                        "title": "اخرین lost ",
                        "metric": f"{random.uniform(0, 1):,.2f}",
                        "footer": mark_safe(
                            f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;میزان تغییرات به درصد'
                        ),
                        "chart": json.dumps(
                            {
                                "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                                "datasets": [{"data": average, "borderColor": "#9333ea"}],
                            }
                        ),
                    },
                    {
                        "title": "اخرین accuracy ",
                        "metric": f"{random.uniform(0, 1):,.2f}",
                        "footer": mark_safe(
                            f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;میزان تغییرات به درصد'
                        ),
                    },
                    
                ],
                "performance": [
                    {
                        # "title": _(" accuracy نمودار",),

                        "metric":"نمودار accuracy ",
                        "footer": mark_safe(
                            '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;میزان تغییرات به درصد'
                        ),
                        "chart": json.dumps(
                            {
                                "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                                "datasets": [
                                    {"data": performance_positive,
                                        "borderColor": "#9333ea"}
                                ],
                            }
                        ),
                    },
                    {
                        # "title": _(" lost نمودار",),

                        "metric": "نمودار lost ",
                        "footer": mark_safe(
                            '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;میزان تغییرات به درصد'
                        ),
                        "chart": json.dumps(
                            {
                                "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                                "datasets": [
                                    {"data": performance_negative,
                                        "borderColor": "#f43f5e"}
                                ],
                            }
                        ),
                    },
                ],
            },
        )


        return context



class ClientDataAdmin(ModelAdmin):
    list_display = ('description',"id", 'is_processed',  'status','redirect_button'
                    ,'start_button'
                    ,'repeat_count'
                    ,'time_repeated'
                    ,'repeated_count'
                    )  # Fields to display in the admin list view
    list_filter = ('status','upload_time')  # Filter data by status
    search_fields = ('description',)  # Allow searching by description
    ordering = ('-upload_time',)  # Default ordering by upload time in descending order
    
    def get_urls(self):
        # Get default admin URLs
        urls = super().get_urls()
        # Add custom URL
        custom_urls = [
            path(
                "chart/<int:id>/",
                MyClassBasedView.as_view(model_admin=self),  # `model_admin` is required for Unfold integration
                name="my_custom_view",
            ),
        ]
        return custom_urls + urls 
    
    def save_model(self, request, obj, form, change):
        # Automatically set the author to the logged-in user on creation
        if not obj.pk:  # If the object is being created
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        # Limit queryset to only show objects created by the logged-in user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        # Allow change permission only if the author matches the logged-in user
        if obj and obj.author != request.user:
            return False
        return super().has_change_permission(request, obj=obj)
    
    def start_button(self, obj):
        # Generate a URL to the specific page
        url = reverse('client_data:generating_model', kwargs={'id': obj.id})
        if obj.is_processed() == False : return  format_html('<a class=" rounded-md bg-primary-600 text-white py-1 flex justify-center" href="{}">شروع   <span class="material-symbols-outlined  pl-2" >play_arrow</span> </a>', url)
        else : return format_html('')
        
    
    start_button.short_description = "شروع آموزش"
    start_button.allow_tags = True  # This line is optional in modern Django
    
    
    def redirect_button(self, obj):
        # Generate a URL to the specific page
        # url = reverse('client_data:generating_model', kwargs={'id': obj.id})
        url = f"/admin/client_data/clientdata/chart/{obj.id}"
        return format_html("""
                           
                           <div> 
                           <a class="  rounded-md bg-primary-600 text-white py-1 px-3" href="{}">مشاهده ی نمودار   </a>
                           </div>
                           """, url)
    
    redirect_button.short_description = " نمودار ها"
    redirect_button.allow_tags = True 
    

admin.site.register(ClientData, ClientDataAdmin)