from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView

from .serializers import RealEstateSpaceSerializer, RealEstateSpacePostSerializer
from ..models import RealEstateSpace


class RealEstateSpaceListAPIView(ListAPIView):
    serializer_class = RealEstateSpaceSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_id', None)
        if project_id is None:
            return RealEstateSpace.objects.all()
        else:
            return RealEstateSpace.objects.filter(project_id=project_id)


real_estate_space_list_api_view = RealEstateSpaceListAPIView.as_view()


class RealEstateSpaceDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RealEstateSpaceSerializer
    queryset = RealEstateSpace.objects.all()

    def get_object(self):
        return super(RealEstateSpaceDetailAPIView, self).get_object()


real_estate_space_detail_api_view = RealEstateSpaceDetailAPIView.as_view()


class RealEstateSpaceCreateAPIView(CreateAPIView):
    serializer_class = RealEstateSpacePostSerializer


real_estate_space_create_api_view = RealEstateSpaceCreateAPIView.as_view()
