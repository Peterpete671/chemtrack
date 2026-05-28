from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import ChemicalSample
from .serializers import ChemicalSampleSerializer
from .analytics import AnalyticsService
from . import response as R

class SampleListCreateView(generics.ListCreateAPIView):
    """
    GET /api/samples/ - List samples with optional filters
    POST /api/samples/ - Create a new sample record
    """
    
    serializer_class = ChemicalSampleSerializer

    def get_queryset(self):
        qs = ChemicalSample.objects.all()
        p = self.request.query_params
        if p.get('sample_type'): qs = qs.filter(sample_type=p['sample_type'])
        if p.get('date_from'): qs = qs.filter(recorded_at__date__gte=p['date_from'])
        if p.get('date_to'): qs = qs.filter(recorded_at__date__lte=p['date_to'])
        if p.get('ph_min'): qs = qs.filter(pH__gte=p['ph_min'])
        if p.get('ph_max'): qs = qs.filter(pH__lte=p['ph_max'])
        if p.get('conc_min'): qs = qs.filter(concentration__gte=p['conc_min'])
        if p.get('conc_max'): qs = qs.filter(concentration__lte=p['conc_max'])
        return qs
    
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        filters_applied = dict(request.query_params)
        return R.ok(
            data=serializer.data,
            endpoint='/api/samples/',
            total_records=qs.count(),
            extra_meta={'filters_applied': filters_applied} if filters_applied else None
        )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return R.created(serializer.data, '/api/samples/')
        return R.error(serializer.errors, '/api/samples/')
    
class SampleDetailView(generics.RetrieveAPIView):
    """GET /api/samples/<id>/ - Retrieve a single sample by ID"""
    queryset = ChemicalSample.objects.all()
    serializer_class = ChemicalSampleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return R.ok(serializer.data, f'api/samples/{instance.id}/')
    
class SummaryView(APIView):
    """
    GET /api/summary/ - Dataset wide and per-type statistical summary
    """
    def get(self, request):
        data = AnalyticsService.get_summary()
        total = data.get('total_records',0)
        return R.ok(data, '/api/summary/', total_records=total)
    
class AnomalyView(APIView):
    """
    GET /api/anomalies/ - Samples flagged as chemically unusual
    """
    
    def get(self, request):
        data = AnalyticsService.get_anomalies()
        return R.ok(
            data=data,
            endpoint='/api/anomalies/',
            total_records=data.get('total_records', 0),
            extra_meta={
                'flagged_count': data.get('flagged_count', 0),
                'flag_rate_pct': data.get('flag_rate_pct, 0'),
            }
        )

class HealthCheckView(APIView):
    """ GET /api/health/ - System status and full endpoint directory"""
    def get(self, request):
        breakdown = {
            item['sample_type']: item['count']
            for item in ChemicalSample.objects
                .values('sample_type')
                .annotate(count=Count('id'))
        }
        return R.ok({
            'system': 'CHEMTRACK',
            'version': 'week-5',
            'records_by_type': breakdown,
            'endpoints': {
                'samples': 'GET /api/samples/ - List and filter records',
                'create': 'POST /api/samples/ - add a new sample',
                'detail': 'GET /api/samples/<id>/ - Retrieve one record',
                'summary': 'GET /api/summary/ - Statistical overview',
                'anomalies': '/api/anomalies/ - Flagged samples',
                'health': 'GET /api/health/ - system status',
            }
        }, endpoint = '/api/health/', total_records=ChemicalSample.objects.count())
    
