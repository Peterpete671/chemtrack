from rest_framework import serializers
from .models import ChemicalSample

#Type-aware pH soft limits

PH_RANGES = {
    'acid': (0.0, 6.9),
    'base': (7.1, 14.0),
    'buffer': (4.0, 10.0),
    'neutral': (6.5, 7.5),
    'unknown': (0.0, 14.0),
}

class ChemicalSampleSerializer(serializers.ModelSerializer):
    concentration_mol_L = serializers.SerializerMethodField()

    def get_concentration_mol_L(self, obj):
         """Explicit unit label for concentration to remove ambiguity"""
         return float(obj.concentration)
    

    class Meta:
        model = ChemicalSample
        fields = [
            'id', 'sample_name', 'sample_type', 'pH',
            'concentration', 'concentration_mol_L', 'temperature', 'notes', 'recorded_at'
        ]
        read_only_fields = ['id', 'recorded_at']

    def validate_concentration(self, value):
        if value <=0:
            raise serializers.ValidationError(
                "Concentration must be greater than 0 mol/L."
            )
        if value > 20:
            raise serializers.ValidationError(
                f"Concentration {value} mol/L exceeds realistic lab range (max 20 mol/L)"
            )
        return value
    
    def validate_temperature(self, value):
        if value is None:
            return value
        if value <-10 or value >200:
            raise serializers.ValidationError(
                f"Temperature {value}C is outside lab-realistic range (-10 to 200C)."
            )
        return value
    
    def validate_sample_name(self, value):
            value = value.strip()
            if not value:
                raise serializers.ValidationError("sample_name cannot be blank.")
            return value
    
    def validate_notes(self, value):
            if len(value) > 500:
                raise serializers.ValidationError(
                    f"Notes cannot exceed 500 characters. Got {len(value)}."
                )
            
            return value
    
    def validate(self, data):
        sample_type = data.get('sample_type')
        pH = data.get('pH')

        if sample_type and pH is not None and sample_type != 'unknown':
            low, high = PH_RANGES[sample_type]
            if not (low <= float(pH) <= high):
                raise serializers.ValidationError({
                    'pH': (
                        f"pH {pH} is inconsistent with sample_type '{sample_type}'."
                        f"Expected range: {low}-{high}."
                        f"Check sample_type or pH value."
                    )
                })
        return data