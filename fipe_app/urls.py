from django.urls import path, include
from .views import ListarMarcasView, ListarModelosView, ListarAnoModelosView, QuilometragemView, CriarLeadView, MostrarPrecificacaoView, IndexView, LeadViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

app_name = 'fipe_app'

router = DefaultRouter()
router.register(r'leads', LeadViewSet)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('listar-marcas/', ListarMarcasView.as_view(), name='listar_marcas'),
    path('listar-modelos/', ListarModelosView.as_view(), name='listar_modelos'),
    path('listar-ano-modelos/', ListarAnoModelosView.as_view(), name='listar_ano_modelos'),
    path('quilometragem/', QuilometragemView.as_view(), name='quilometragem'),
    path('criar-lead/', CriarLeadView.as_view(), name='criar_lead'),
    path('mostrar-precificacao/<int:lead_id>/',MostrarPrecificacaoView.as_view(), name='show_price'),
    path('api/', include(router.urls)),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
