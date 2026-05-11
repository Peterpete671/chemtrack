from django.db.models import Avg, Min, Max, Count
from .models import ChemicalSample

#Type-aware pH thresholds; Centralized here, not duplicated across files
#These define what is "Normal" for each sample type based on Chemistry.

PH_THRESHOLDS = {
    'acid': (0.0, 6.9),
    'base': (7.1, 14.0),
    'buffer': (4.0, 10.0),
    'neutral': (6.5, 7.5),
    'unknown': (0.0, 14.0),
}

CONCENTRATION_MAX_NORMAL = 0.5
TEMPERATURE_STANDARD = 25.0
TEMPERATURE_TOLERANCE = 2.0

class AnalyticsService:
    """
    Computes summary statistics and computes anomalies
    Seperated from views deliberately; HTTP logic belongs in views
    Chemistry logics belong here
    All methods return plain Python dicts for easy JSON serialization
    """

    @staticmethod
    def get_summary():
        """Returns dataset-wide and per-type pH and concentration statistics."""
        total = ChemicalSample.objects.count()
        if total == 0:
            return {'error': 'No records in database.'}
        
        overall = ChemicalSample.objects.aggregate(
            avg_pH=Avg('pH'),
            min_pH=Min('pH'),
            max_pH=Max('pH'),
            avg_concentration=Avg('concentration'),
            total=Count('id')
        )

        by_type = {}
        for stype in ['acid', 'base', 'buffer', 'neutral', 'unknown']:
            qs = ChemicalSample.objects.filter(sample_type=stype)
            count = qs.count()
            if count == 0:
                continue
            agg = qs.aggregate(
                avg_pH=Avg('pH'),
                min_pH=Avg('pH'),
                max_pH=Max('pH'),
                avg_conc=Avg('concentration')
            )
            by_type[stype] = {
                'count': count,
                'avg_pH': round(float(agg['avg_pH']), 2),
                'min_pH': round(float(agg['min_pH']), 2),
                'max_pH': round(float(agg['max_pH']), 2),
                'avg_conc_mol_L': round(float(agg['avg_conc']), 4),
            }

            return{
                'total_records': overall['total'],
                'overall': {
                    'avg_pH': round(float(overall['avg_pH']), 2),
                    'min_pH': round(float(overall['min_pH']), 2),
                    'max_pH': round(float(overall['max_pH']), 2),
                    'avg_concentration': round(float(overall['avg_concentration']), 4),
                },
                'by_sample_type': by_type,
            }
        
    @staticmethod
    def get_anomalies():
        """
        Flags samples that deviate from the expected chemical behaviour
        3 Flag types:
        1. pH outside the expected range for the sample type
        2. Concentration above the normal threshold of 0.5 mol/L
        3. Temperature more than 2C from standard 25C
        Returns samples sorted by flag_count descending, worst first.
        A flag does not mean that the data is wrong, but is unusual and warrants review by chemist
        """

        flagged = []

        for sample in ChemicalSample.objects.all():
            reasons = []
            stype = sample.sample_type

            #Flag 1: pH outside expected range for this type
            if stype in PH_THRESHOLDS and stype != 'unknown':
                low, high = PH_THRESHOLDS[stype]
                ph = float(sample.pH)
                if not (low <= ph <= high):
                    reasons.append(
                        f"pH {ph} is outside expected range {low} - {high} for '{stype}'"
                    )

            #Flag 2: unusually high concentration
            conc = float(sample.concentration)
            if conc > CONCENTRATION_MAX_NORMAL:
                reasons.append(
                    f"Concentration {conc} mol/L exceeds normal threshold "
                    f"({CONCENTRATION_MAX_NORMAL} mol/L)"
                )

            #Flag 3: non-standard measurement temperature
            if sample.temperature is not None:
                temp = float(sample.temperature)
                deviation = abs(temp - TEMPERATURE_STANDARD)
                if deviation > TEMPERATURE_TOLERANCE:
                    reasons.append(
                        f"Temperature {temp}C deviates {round(deviation, 1)}C"
                        f"from standard {TEMPERATURE_STANDARD}C"
                    )

            if reasons:
                flagged.append({
                    'id': sample.id,
                    'sample_name': sample.sample_name,
                    'sample_type': sample.sample_type,
                    'pH': float(sample.pH),
                    'concentration': float(sample.concentration),
                    'temperature': float(sample.temperature) if sample.temperature else None,
                    'recorded_at': sample.recorded_at.isoformat(),
                    'flags': reasons,
                    'flag_count': len(reasons),
                })

        total = ChemicalSample.objects.count()
        return {
            'total_records': total,
            'flagged_count': len(flagged),
            'flag_rate_pct': round(len(flagged) / max(total, 1) * 100, 1),
            'anomalies': sorted(flagged, key=lambda x: x['flag_count'], reverse=True),
        }
            