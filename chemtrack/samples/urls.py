from django.urls import path
from .views import SampleListCreateView, SampleDetailView, HealthCheckView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('samples/', SampleListCreateView.as_view(), name='sample-list-create'),
    path('samples/<int:pk>/', SampleDetailView.as_view(), name='sample-detail'),
]