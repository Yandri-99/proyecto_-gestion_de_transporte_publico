from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from transporte.views.health   import health_check, health_check_cicd
from transporte.views.auth     import RegisterView, LogoutView
from transporte.views.user     import UserViewSet
from transporte.views.route    import RouteViewSet
from transporte.views.bus      import BusViewSet
from transporte.views.driver   import DriverViewSet
from transporte.views.trip     import TripViewSet
from transporte.views.ticket   import TicketViewSet
from transporte.serializers.auth import CustomTokenView

router = DefaultRouter()
router.register('users',      UserViewSet,    basename='user')
router.register('routes',     RouteViewSet,   basename='route')
router.register('buses',      BusViewSet,     basename='bus')
router.register('drivers',    DriverViewSet,  basename='driver')
router.register('trips',      TripViewSet,    basename='trip')
router.register('tickets',    TicketViewSet,  basename='ticket')

urlpatterns = [
    path('health/',             health_check),
    path('health/cicd/',        health_check_cicd),
    path('auth/register/',      RegisterView.as_view()),
    path('auth/login/',         CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/',  TokenVerifyView.as_view()),
    path('auth/logout/',        LogoutView.as_view()),
    path('', include(router.urls)),
]
