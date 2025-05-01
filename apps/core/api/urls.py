from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TweetViewSet

router = DefaultRouter()
router.register(r"tweets", TweetViewSet, basename="tweet")

urlpatterns = [
    path("", include(router.urls)),
]
