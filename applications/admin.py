from django.conf import settings
from django.contrib import admin
# Register your models here.
from django.contrib.auth.decorators import login_required
from django.utils.timesince import timesince

from applications import models

import csv
from django.http import HttpResponse

EXPORT_CSV_FIELDS = ['name', 'email', 'phone_number', 'university', 'gender','other_gender','ethnicity','other_ethnicity','degree', 'education', 'graduation_year', 'data_consent', 'referral','resume','sponsor_consent']

EXPORT_CSV_FOR_MLH = ['name', 'email', 'phone_number', 'university', 'gender','other_gender','ethnicity','other_ethnicity','degree', 'education', 'graduation_year', 'data_consent']

EXPORT_CSV_FOR_SPONSOR = ['name', 'email', 'university', 'degree', 'education', 'graduation_year', 'resume', 'sponsor_consent']

EXPORT_CSV_FOR_FOOD = ['name', 'email', 'university', 'diet', 'other_diet']

EXPORT_CSV_FOR_SENDY = ['name','email','first_timer']


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'votes', 'reimb', 'status',
                    'status_last_updated', 'diet')
    list_filter = ('status', 'first_timer', 'reimb', 'graduation_year',
                   'university', 'origin', 'under_age', 'diet','sponsor_consent')
    list_per_page = 200
    search_fields = ('user__name', 'user__email',
                     'description',)
    ordering = ('submission_date',)
    date_hierarchy = 'submission_date'

    actions = ["export_as_csv", "export_as_sendy", "export_as_MLH", "export_as_sponsor","export_as_food"]

    def export_csv(self, request, queryset, filename, fields):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(filename)
        writer = csv.writer(response)

        writer.writerow(fields)
        for obj in queryset:
            row = []
            for field in fields:
                if hasattr(getattr(obj,'user'),field):
                    row.append(getattr(getattr(obj,'user'),field))
                else:
                    row.append(getattr(obj,field))
            written = writer.writerow(row)
        return response

    def export_as_csv(self, request, queryset):
        return self.export_csv(request,queryset,"hackers",EXPORT_CSV_FIELDS)
    export_as_csv.short_description = "Export to All CSV"

    def export_as_sendy(self, request, queryset):
        return self.export_csv(request,queryset,"sendy",EXPORT_CSV_FOR_SENDY)
    export_as_sendy.short_description = "Export to Sendy CSV"

    def export_as_MLH(self, request, queryset):
        return self.export_csv(request,queryset,"mlh",EXPORT_CSV_FOR_MLH)
    export_as_MLH.short_description = "Export to MLH CSV"

    def export_as_sponsor(self, request, queryset):
        return self.export_csv(request,queryset,"sponsor",EXPORT_CSV_FOR_SPONSOR)
    export_as_sponsor.short_description = "Export to Sponsor CSV"

    def export_as_food(self, request, queryset):
        return self.export_csv(request,queryset,"food",EXPORT_CSV_FOR_FOOD)
    export_as_food.short_description = "Export to Food CSV"

    def name(self, obj):
        return obj.user.get_full_name() + ' (' + obj.user.email + ')'

    name.admin_order_field = 'user__name'  # Allows column order sorting
    name.short_description = 'Hacker info'  # Renames column head

    def votes(self, app):
        return app.vote_avg

    votes.admin_order_field = 'vote_avg'

    def status_last_updated(self, app):
        if not app.status_update_date:
            return None
        return timesince(app.status_update_date)

    status_last_updated.admin_order_field = 'status_update_date'

    def get_queryset(self, request):
        qs = super(ApplicationAdmin, self).get_queryset(request)
        return models.Application.annotate_vote(qs)


admin.site.register(models.Application, admin_class=ApplicationAdmin)
admin.site.site_header = '%s Admin' % settings.HACKATHON_NAME
admin.site.site_title = '%s Admin' % settings.HACKATHON_NAME
admin.site.index_title = 'Home'
admin.site.login = login_required(admin.site.login)
