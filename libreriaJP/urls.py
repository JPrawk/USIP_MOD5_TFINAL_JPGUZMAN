from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from libros.views import GeneroViewSet, AutorViewSet, LibroViewSet, ArchivoLibroViewSet
from doc_tecnicos.views import OrganismoNormaViewSet, DocumentoTecnicoViewSet

router = DefaultRouter()
router.register(r'generos', GeneroViewSet)
router.register(r'autores', AutorViewSet)
router.register(r'libros', LibroViewSet)
router.register(r'archivos', ArchivoLibroViewSet)
router.register(r'organismos', OrganismoNormaViewSet)
router.register(r'documentos', DocumentoTecnicoViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='LibreriaJP API',
        default_version='v1',
        description='API para gestión de librería digital',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)