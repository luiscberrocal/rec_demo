from rest_framework import serializers

#
# class $MODEL_NAME$PostSerializer(serializers.ModelSerializer):
#     """
#     Standard Serializer for $MODEL_NAME$ model.
#     """
#
#     class Meta:
#         model = $MODEL_NAME$
#         fields = ('id')
#
#
# class $MODEL_NAME$rSerializer($MODEL_NAME$PostSerializer):
#     """
#     Standard Serializer for $MODEL_NAME$ model.
#     """
#     pass
from ..models import RealEstateSpace


class RealEstateSpacePostSerializer(serializers.ModelSerializer):
    """
    Standard Serializer for RealEstateSpace model.
    """

    class Meta:
        model = RealEstateSpace
        fields = (
            'id', 'project', 'name', 'space_type', 'area', 'price', 'contract', 'created', 'modified', 'created_by',
            'modified_by',
        )


class RealEstateSpaceSerializer(RealEstateSpacePostSerializer):
    """
    Standard Serializer for RealEstateSpace model.
    """
    pass
