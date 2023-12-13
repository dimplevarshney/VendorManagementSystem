from rest_framework import serializers
from .models import HistoricalPerformance

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = "__all__"