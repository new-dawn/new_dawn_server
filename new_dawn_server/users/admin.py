from django.contrib import admin
from new_dawn_server.medias.models import Image
from new_dawn_server.questions.models import AnswerQuestion
from new_dawn_server.users.models import Account
from new_dawn_server.users.models import Profile

# The profile page will be used as review tool
class ImageInline(admin.TabularInline):
    model = Image
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]
    def has_add_permission(self, request, obj=None):
        return False

class AnswerQuestionInline(admin.TabularInline):
    model = AnswerQuestion
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]
    def has_add_permission(self, request, obj=None):
        return False

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('review_status',)
    inlines = [
        ImageInline,
        AnswerQuestionInline,
    ]
    fields = (
        'review_status',
        'age',
        'degree',
        'drink',
        'employer',
        'height',
        'hometown',
        'job_title',
        'school',
        'smoke'
    )
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields if f.name != 'review_status']
    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Account)
admin.site.register(Profile, ProfileAdmin)