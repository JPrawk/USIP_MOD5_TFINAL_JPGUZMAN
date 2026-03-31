from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from libros.views import (
    CategoriaViewSet as LibrosCategoriaViewSet,
    GeneroViewSet,
    AutorViewSet,
    LibroViewSet,
    ArchivoLibroViewSet,
    reporte_libros,
    inicio,
    libros_lista,
    libros_detalle,
    autores_lista,
)
from doc_tecnicos.views import (
    CategoriaViewSet as DocCategoriaViewSet,
    OrganismoNormaViewSet,
    DocumentoTecnicoViewSet,
    LibroIngElectricaViewSet,
    reporte_documentos,
    documentos_lista,
    documentos_detalle,
    organismos_lista,
)

router = DefaultRouter()

# libros
router.register(r'libros/categorias', LibrosCategoriaViewSet, basename='libros-categoria')
router.register(r'generos', GeneroViewSet, basename='genero')
router.register(r'autores', AutorViewSet, basename='autor')
router.register(r'libros', LibroViewSet, basename='libro')
router.register(r'archivos', ArchivoLibroViewSet, basename='archivo')

# doc_tecnicos
router.register(r'doc/categorias', DocCategoriaViewSet, basename='doc-categoria')
router.register(r'organismos', OrganismoNormaViewSet, basename='organismo')
router.register(r'documentos', DocumentoTecnicoViewSet, basename='documento')
router.register(r'libros-ing', LibroIngElectricaViewSet, basename='libro-ing')

schema_view = get_schema_view(
    openapi.Info(
        title='LibreriaJP API',
        default_version='v1',
        description='API para gestión de librería digital',
        contact=openapi.Contact(email='contacto@libreriajp.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Vistas HTML
    path('', inicio, name='inicio'),
    path('libros/', libros_lista, name='libros_lista'),
    path('libros/<int:pk>/', libros_detalle, name='libros_detalle'),
    path('autores/', autores_lista, name='autores_lista'),
    path('documentos/', documentos_lista, name='documentos_lista'),
    path('documentos/<int:pk>/', documentos_detalle, name='documentos_detalle'),
    path('organismos/', organismos_lista, name='organismos_lista'),

    # API REST
    path('api/', include(router.urls)),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Reportes
    path('api/reporte/libros/', reporte_libros, name='reporte_libros'),
    path('api/reporte/documentos/', reporte_documentos, name='reporte_documentos'),

    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)