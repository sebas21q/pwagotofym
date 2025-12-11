from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Category, Post, ProductCategory, Product, ColorMarca

# encabezados del admin
admin.site.site_header = "GoToGym Admin"
admin.site.site_title = "Panel GoToGym"
admin.site.index_title = "Administración del sitio"

# --- USER ---
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # mostrar 'plan' en la lista
    list_display = DjangoUserAdmin.list_display + ("plan",)

    # permitir editar 'plan' en el formulario del usuario
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Suscripción", {"fields": ("plan",)}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (None, {"fields": ("plan",)}),
    )

# --- BLOG ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("title",)

# --- PRODUCTS ---
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    list_filter = ("category",)
    search_fields = ("name",)

# --- CONFIGURACION_MARCA ---
@admin.register(ColorMarca)
class ColorMarcaAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_code")
    search_fields = ("name", "hex_code")
