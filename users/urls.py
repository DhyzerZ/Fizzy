from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet
from .views import MyTokenObtainPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]