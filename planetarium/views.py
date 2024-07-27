from rest_framework import views, mixins
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrIfAuthenticatedReadOnly

from .models import (
    PlanetariumDome,
)
from .serializers import (
    PlanetariumDomeSerializer
)


class PlanetariumDomeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
