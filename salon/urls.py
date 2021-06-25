from django.contrib import admin
import debug_toolbar
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi


# schema_view = get_schema_view(
#    openapi.Info(
#       title = "",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="Test License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #Oauth
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),

    # users
    path('api/users/', include('users.urls', namespace='users' )),
    
        # django rest web login
    path('api_auth/', include('rest_framework.urls', namespace='rest_framework')),

    # documentation
    path('', include_docs_urls(title='SalonAPI')),
    path('schema', get_schema_view(title="SalonAPI", description="API for the SalonAPI",version="1.0.0"), name='openapi-schema'),
    
    # #swagger documentation
    # path('', schema_view.with_ui('swagger', cache_timeout=0, ), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns =[

        # debug toolbar
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
