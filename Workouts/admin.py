from django.contrib import admin
from .models import MuscleGroup, SubMuscle, Exercise
from django.utils.html import format_html

# 🔹 SubMuscles inline inside MuscleGroup
class SubMuscleInline(admin.TabularInline):
    model = SubMuscle
    extra = 1

    # 🔥 SHOW IMPORTANT FIELDS
    fields = ('name', 'description', 'video')

    # optional: make UI cleaner
    show_change_link = True


# 🔹 MuscleGroup admin
class MuscleGroupAdmin(admin.ModelAdmin):
    inlines = [SubMuscleInline]
    list_display = ('name', 'preview_image')

    from django.utils.html import format_html

class MuscleGroupAdmin(admin.ModelAdmin):
    inlines = [SubMuscleInline]
    list_display = ('name', 'preview_image')
    search_fields = ('name',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:8px;" />', obj.image.url)
        return "No Image"
    


admin.site.register(MuscleGroup, MuscleGroupAdmin)


# 🔹 SubMuscle admin (FULL CONTROL PAGE)
class SubMuscleAdmin(admin.ModelAdmin):
    list_display = ('name', 'muscle_group', 'preview_image', 'short_description')
    list_filter = ('muscle_group',)
    search_fields = ('name', 'description')

    def short_description(self, obj):
        return (obj.description[:40] + "...") if obj.description else "No description"

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:8px;" />',
                obj.image.url
            )
        return "No Image"


admin.site.register(SubMuscle, SubMuscleAdmin)


# 🔹 Exercise admin
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_muscle')
    list_filter = ('sub_muscle',)
    search_fields = ('name',)


admin.site.register(Exercise, ExerciseAdmin)