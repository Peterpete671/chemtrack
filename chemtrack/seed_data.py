"""
Usage:
python manage.py shell < seed_data.py
These entries reflect real lab scenarios, and not random numbers
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemtrack.settings')
django.setup()

from samples.models import ChemicalSample

entries = [
    #Acids
    {
        "sample_name": "ACD-001-AK",
        "sample_type": "acid",
        "pH": "2.10",
        "concentration": "0.1000",
        "temperature": "25.00",
        "notes": "Hydrochloric acid standard. Freshly prepared."
    },
    {
        "sample_name": "ACD-002-AK",
        "sample_type": "acid",
        "pH": "3.75",
        "concentration": "18.00",
        "notes": "Acetic acid solution. Slight turbidity noted."
    },
    {
        "sample_name": "ACD-003-AK",
        "sample_type": "acid",
        "pH": "1.20",
        "concentration": "0.100",
        "temperature": "25.00",
        "notes": "Sulfuric acid - Handle with care. Double checked concentration."
    },
    
    #Bases

    {
        "sample_name": "BAS-001-AK",
        "sample_type": "base",
        "pH": "12.50",
        "concentration": "0.1000",
        "temperature": "25.00",
        "notes": "Sodium Hydroxide Solution. Standard 0.1M Solution"
    },
    {
        "sample_name": "BAS-002-AK",
        "sample_type": "base",
        "pH": "10.80",
        "concentration": "0.0250",
        "temperature": "26.00",
        "notes":"Ammonia solution. Lab temp slightly elevated today."
    },
    #Buffers
    {
        "sample_name": "BUF-001-AK",
        "sample_type": "buffer",
        "pH": "7.00",
        "concentration": "0.1000",
        "temperature": "25.00",
        "notes": "Phosphate buffer. pH callibration reference."
    },
    {
        "sample_name": "BUF-002-AK",
        "sample_type": "buffer",
        "pH": "4.01",
        "concentration": "0.1000",
        "temperature": "25.00",
        "notes": "Acetate buffer. Used as low-pH reference standard."
    },
    {
        "sample_name": "BUF-003-AK",
        "sample_type": "buffer",
        "pH": "9.20",
        "concentration": "0.0500",
        "temperature": "23.80",
        "notes": "Borate buffer. Slightly below room temperature, recorded accurately."
    },
    #Neutral
    {
        "sample_name": "NEU-001-AK",
        "sample_type": "neutral",
        "pH": "6.98",
        "concentration": "0.0100",
        "temperature": "25.00",
        "notes": "Distilled water sample. Near neutral as expected."
    },

    #Unknown
    {
        "sample_name": "UNK-001-AK",
        "sample_type": "unknown",
        "pH": "5.60",
        "concentration": "0.0200",
        "temperature": None,
        "notes": "Unidentified sample from storage. Temperature not recorded, assuming 25C"
    },
]

created = 0
for entry in entries:
    exists = ChemicalSample.objects.filter(sample_name=entry["sample_name"]).exists()
    if exists:
        print(f"  Skipped (exists): {entry['sample_name']}")
        continue
    obj = ChemicalSample.objects.create(**entry)
    print(f"  Created: {obj}")
    created += 1

print(f"\nDone. {created} new record(s) created. Total in DB: {ChemicalSample.objects.count()}")