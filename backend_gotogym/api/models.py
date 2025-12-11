from django.contrib.auth.models import AbstractUser
from django.db import models

# --- USUARIO PERSONALIZADO (solo UNA vez) ---
class User(AbstractUser):
    plan = models.CharField(
        max_length=20,
        choices=[("Gratis", "Gratis"), ("Premium", "Premium")],
        default="Gratis"
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username

# --- BLOG ---
class Category(models.Model):
    name = models.CharField("Nombre", max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categorys"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField("Título", max_length=150)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title

# --- PRODUCTS ---
class ProductCategory(models.Model):
    name = models.CharField("Nombre", max_length=100)

    class Meta:
        verbose_name = "Product category"
        verbose_name_plural = "Product categorys"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField("Nombre", max_length=150)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField("Precio", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

# --- CONFIGURACION_MARCA ---
class ColorMarca(models.Model):
    name = models.CharField("Nombre", max_length=50)
    hex_code = models.CharField("Color (HEX)", max_length=7)  # ej: #FF0000

    class Meta:
        verbose_name = "Color marcas"
        verbose_name_plural = "Color marcas"

    def __str__(self):
        return f"{self.name} ({self.hex_code})"
