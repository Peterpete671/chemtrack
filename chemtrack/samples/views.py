from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ChemicalSample
from .serializers import ChemicalSampleSerializer

class SampleListCreateView(generics.ListCreateAPIView):
    """
    GET /api/samples/ - List all samples with optional filters
    POST /api/samples/ - Create a new sample
    
    supported query parameters:
    sample_type - acid|base|buffer|neutral|unknown
    date_from - YYYY-MM-DD
    date_to - YYYY-MM-DD
    ph_min - decimal
    ph_max - decimal
    conc_min - decimal
    conc_max - decimal
    """

    serializer_class = ChemicalSampleSerializer

    def get_queryset(self):
        qs = ChemicalSample.objects,all()
        params = self.request.query_params

        sample_type = params.get('sample_type')
        if sample_type:
            qs = qs.filter(sample_type=sample_type)

        date_from = params.get('date_from')
        date_to = params.get('date_to')
        if date_from:
            qs = qs.filter(recorded_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(recorded_at__date__lte=date_to)

        ph_min = params.get('ph_min')
        ph_max = params.get('ph_max')
        if ph_min:
            qs = qs.filter(pH__gte=ph_min)
        if ph_max:
            qs = qs.filter(pH__lte=ph_max)

        conc_min = params.get('conc_min')
        conc_max = params.get('conc_max')

        if conc_min:
            qs = qs.filter(concentration__gte=conc_min)
        if conc_max:
            qs = qs.filter(concentration__lte=conc_max)

        return qs
    
class SampleDetailView(generics.RetrieveAPIView):
    queryset = ChemicalSample.objects.all()
    serializer_class = ChemicalSampleSerializer

class HealthCheckView(APIView):
    def get(self, request):
        count = ChemicalSample.objects.count()
        return Response({
            'status': 'ok',
            'system': 'CHEM-TRACK',
            'week': 2,
            'total_records': count
        }, status=status.HTTP_200_OK)
