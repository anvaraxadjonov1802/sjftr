from django.contrib import admin
from .models import (
    NazariyMavzular, AmaliyMavzular, Masalalar,
    Videolar, Test, TestSavol, TestNatija
)


@admin.register(NazariyMavzular)
class NazariyMavzularAdmin(admin.ModelAdmin):
    list_display = ('tartib_raqami', 'mavzu', 'word_file')
    search_fields = ('mavzu',)
    ordering = ('tartib_raqami',)


@admin.register(AmaliyMavzular)
class AmaliyMavzularAdmin(admin.ModelAdmin):
    list_display = ('tartib_raqami', 'mavzu', 'nazariy_mavzu', 'word_file')
    search_fields = ('mavzu', 'nazariy_mavzu__mavzu')
    list_filter = ('nazariy_mavzu',)
    ordering = ('tartib_raqami',)


@admin.register(Masalalar)
class MasalalarAdmin(admin.ModelAdmin):
    list_display = ('tartib_raqami', 'mavzu', 'word_file')
    search_fields = ('mavzu',)
    ordering = ('tartib_raqami',)


@admin.register(Videolar)
class VideolarAdmin(admin.ModelAdmin):
    list_display = ('tartib_raqami', 'sarlavha', 'nazariy_mavzu')
    list_filter = ('nazariy_mavzu',)
    search_fields = ('sarlavha',)


class TestSavolInline(admin.TabularInline):
    model = TestSavol
    extra = 0


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('tartib_raqami', 'sarlavha', 'nazariy_mavzu')
    search_fields = ('sarlavha', 'nazariy_mavzu__mavzu')
    list_filter = ('nazariy_mavzu',)
    ordering = ('tartib_raqami',)
    inlines = [TestSavolInline]


@admin.register(TestSavol)
class TestSavolAdmin(admin.ModelAdmin):
    list_display = ('test', 'savol_matni', 'togri_javob')
    search_fields = ('savol_matni', 'test__sarlavha')
    list_filter = ('test', 'togri_javob')


@admin.register(TestNatija)
class TestNatijaAdmin(admin.ModelAdmin):
    list_display = (
        'foydalanuvchi', 'test', 'togri_savollar_soni',
        'jami_savollar_soni', 'foiz', 'yakunlangan_vaqt'
    )
    search_fields = ('foydalanuvchi__username', 'test__sarlavha')
    list_filter = ('test', 'yakunlangan_vaqt')
    ordering = ('-yakunlangan_vaqt',)
