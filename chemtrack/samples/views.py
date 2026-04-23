from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ChemicalSample
from .serializers import ChemicalSampleSerializer
# Create your views here.


class SampleListCreateView(generics.ListCreateAPIView):
    """
    GET /api/samples/ - retrieve all samples (Newest First)
    POST /api/samples/ - create a new sample record
    
    Week 1 scope: no filtering yet
    """

    queryset = ChemicalSample.objects.all()
    serializer_class = ChemicalSampleSerializer

class SampleDetailView(generics.RetrieveAPIView):
    """
    GET /api/samples/<id>/ - Retrieve a single sample by ID
    """
    queryset = ChemicalSample.objects.all()
    serializer_class = ChemicalSampleSerializer

class HealthCheckView(APIView):
    """
    GET /api/health/ - confirms the system is running
    Verifies setup before inputing real data
    """
    def get(self, request):
        count = ChemicalSample.objects.count()
        return Response({
            "status": "ok",
            "system": "CHEM-TRACK",
            "week": 1,
            "total_records": count,
            "message": f"System live. {count} sample(s) stored."
        }, status=status.HTTP_200_OK)