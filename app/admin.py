from django.contrib import admin
from .models import *
from django.db.models import Sum, Count
# Register your models here.


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('username', 'image_tag', 'created_at', 'last_updated')
    search_fields = ('username', 'email', )
    list_filter = ('created_at',)


@admin.register(UserSummary)
class UserSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/user_added_summary.html'
    date_hierarchy = 'created_at'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
        'total': Count('username'),
        }

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        return response


@admin.register(Hits)
class HitsAdmin(admin.ModelAdmin):
    search_fields = ('key', 'value', )
    list_display = ('key', 'value', 'created_at')


@admin.register(HitsSummary)
class HitsSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/hits_sum.html'
    date_hierarchy = 'created_at'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
        'total': Sum('value'),
        }

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        return response
