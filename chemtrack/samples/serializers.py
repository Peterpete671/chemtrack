from rest_framework import serializers
from .models import ChemicalSample

class ChemicalSampleSerializer(serializers.ModelSerializer):
    """
    Serializer for ChemicalSample

    Week 1: basic field mapping plus core type validation
    Week 2: cross-field rules, range checks, anomaly flags
    """

    class Meta:
        model = ChemicalSample
        fields = [
            'id',
            'sample_name',
            'sample_type',
            'pH',
            'concentration',
            'temperature',
            'notes',
            'recorded_at',
        ]
        read_only_fields = ['id', 'recorded_at']

        #Basic validations

        def validate_sample_name(self, value):
            value = value.strip()
            if not value:
                raise serializers.ValidationError("sample_name cannot be blank.")
            return value
        
        def validate_pH(self, value):
            if value  < 0 or value > 14:
                raise serializers.ValidationError(
                    f"pH must be between 0 and 14. Got {value}"
                )
            return value
        
        def validate_concentration(self, value):
            if value <= 0:
                raise serializers.ValidationError(
                    "Concentration must be greater than 0 mol/L."
                )
            return value
        
        def validate_notes(self, value):
            if len(value) > 500:
                raise serializers.ValidationError(
                    f"Notes cannot exceed 500 characters. Got {len(value)}."
                )
            
            return value