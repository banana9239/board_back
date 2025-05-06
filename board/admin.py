from django.contrib import admin
from .models import Board, LargeCategory, MediumCategory, SmallCategory


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['board_name', 'board_category', 'created_at', 'updated_at']

@admin.register(LargeCategory)
class LargeCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(MediumCategory)
class MediumCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(SmallCategory)
class SmallCategoryAdmin(admin.ModelAdmin):
    pass
