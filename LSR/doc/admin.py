from django.contrib import admin
from .models import Letter


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'content',
        'send_date'
    )
    list_editable = (
        'content',
    )
    search_fields = ('number',)
    list_filter = ('send_date',)
    

admin.site.register(Letter, PostAdmin)