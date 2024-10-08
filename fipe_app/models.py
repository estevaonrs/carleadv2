from django.db import models
from django.utils import timezone
from django.utils.formats import number_format

class Lead(models.Model):
    mileage = models.IntegerField(verbose_name="Quilometragem")
    name = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail")
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    brand = models.CharField(max_length=255, verbose_name="Marca")
    model = models.CharField(max_length=100, verbose_name="Modelo")
    year = models.CharField(max_length=100, verbose_name="Ano")
    fuel = models.CharField(max_length=100, verbose_name="Combustível")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço")
    market_category = models.CharField(max_length=50, null=True, blank=True, verbose_name="Categoria de Mercado")
    car_category = models.CharField(max_length=50, null=True, blank=True, verbose_name="Categoria do Veículo")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço Original")
    pricing_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Percentual de Preço")
    revisions_done_in_css = models.BooleanField(default=False, verbose_name="Revisões Feitas no CSS")
    under_warranty = models.BooleanField(default=False, verbose_name="Está na Garantia?")
    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Data de Criação")

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email} - {self.phone}"

    def formatted_price(self):
        if self.price:
            return "R$ " + number_format(self.price, 2, force_grouping=True, use_l10n=True)
        return "Preço não informado"

    def formatted_original_price(self):
        if self.original_price:
            return "R$ " + number_format(self.original_price, 2, force_grouping=True, use_l10n=True)
        return "Preço original não informado"

    def pricing_percentage_display(self):
        if self.pricing_percentage is not None:
            return f"{self.pricing_percentage * 100}%"
        return "Percentual de preço não informado"

    @property
    def full_car_description(self):
        """Retorna uma descrição completa do veículo."""
        return f"{self.brand} {self.model} ({self.year}) - {self.fuel}"

