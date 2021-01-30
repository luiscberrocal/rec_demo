from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView

from .serializers import RealEstateSpaceSerializer, RealEstateSpacePostSerializer, ContractSerializer
from ..models import RealEstateSpace, Contract


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


class ContractListAPIView(ListAPIView):
    serializer_class = ContractSerializer

    def get_queryset(self):
        return Contract.objects.all()


contract_list_api_view = ContractListAPIView.as_view()


class ContractDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()

    def get_object(self):
        return super(ContractDetailAPIView, self).get_object()


contract_detail_api_view = ContractDetailAPIView.as_view()


class ContractCreateAPIView(CreateAPIView):
    serializer_class = ContractSerializer


contract_create_api_view = ContractCreateAPIView.as_view()
