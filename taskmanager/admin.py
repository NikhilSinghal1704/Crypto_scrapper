from django.contrib import admin
from .models import ScrapingJob, CoinData

class CoinDataInline(admin.TabularInline):
    model = CoinData
    extra = 0

@admin.register(ScrapingJob)
class ScrapingJobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('job_id',)
    date_hierarchy = 'created_at'
    inlines = [CoinDataInline]

@admin.register(CoinData)
class CoinDataAdmin(admin.ModelAdmin):
    list_display = ('coin', 'job')
    list_filter = ('coin',)
    search_fields = ('coin', 'output')
    autocomplete_fields = ['job']