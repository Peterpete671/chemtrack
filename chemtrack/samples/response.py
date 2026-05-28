"""
Standardized response helpers for all CHEMTRACK endpoints

Every API response follows the same envelope:
{"status": "ok"|"error"|"created", "meta": {...}, "data":{...} }
"""

from rest_framework.response import Response
from rest_framework import status as http_status

def ok(data, endpoint, total_records=None, extra_meta=None):
    """Standard 200 success response"""
    meta = {'endpoint': endpoint}
    if total_records is not None:
        meta['total_records']= total_records
    if extra_meta:
        meta.update(extra_meta)
    return Response({
        'status': 'ok',
        'meta': meta,
        'data': data,
    },status=http_status.HTTP_200_OK)

def created(data, endpoint):
    """Standard 201 created response.""" 
    return Response({
        'status': 'created',
        'meta': {'endpoint': endpoint},
        'data': data,
    }, status=http_status.HTTP_201_CREATED)

def error(errors, endpoint, status_code=400):
    """Standard 400 error response"""
    return Response({
        'status': 'error',
        'meta': {'endpoint': endpoint},
        'errors': errors,
    }, status=status_code)