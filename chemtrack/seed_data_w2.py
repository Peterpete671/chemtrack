"""
seed_data_w2.py — Week 2 expanded dataset (30 additional entries)
Run: python manage.py shell < seed_data_w2.py

Adds realistic variation across all 5 sample types.
Safe to run multiple times — skips existing sample_names.
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemtrack.settings')
django.setup()

from samples.models import ChemicalSample

entries = [
    # ACIDS (8 entries)
    {'sample_name':'ACD-004-AK','sample_type':'acid','pH':'4.20','concentration':'0.0500','temperature':'25.00','notes':'Weak acid. Acetic acid dilute solution.'},
    {'sample_name':'ACD-005-AK','sample_type':'acid','pH':'2.80','concentration':'0.2500','temperature':'24.00','notes':'Phosphoric acid partial neutralisation.'},
    {'sample_name':'ACD-006-AK','sample_type':'acid','pH':'1.50','concentration':'0.5000','temperature':'25.00','notes':'Strong acid — HCl concentrated.'},
    {'sample_name':'ACD-007-AK','sample_type':'acid','pH':'5.10','concentration':'0.0100','temperature':'23.50','notes':'Dilute carbonic acid. Prepared from CO2 dissolution.'},
    {'sample_name':'ACD-008-AK','sample_type':'acid','pH':'3.30','concentration':'0.1500','temperature':'25.00','notes':'Citric acid solution. Food-grade source.'},
    {'sample_name':'ACD-009-AK','sample_type':'acid','pH':'6.20','concentration':'0.0050','temperature':'25.00','notes':'Very dilute acid. Near-neutral but confirmed acid.'},
    {'sample_name':'ACD-010-AK','sample_type':'acid','pH':'2.10','concentration':'0.3000','temperature':'26.00','notes':'Nitric acid. Lab temp slightly elevated.'},
    {'sample_name':'ACD-011-AK','sample_type':'acid','pH':'4.80','concentration':'0.0750','temperature':'25.00','notes':'Lactic acid biological sample.'},

    # BASES (8 entries)
    {'sample_name':'BAS-003-AK','sample_type':'base','pH':'11.50','concentration':'0.0500','temperature':'25.00','notes':'Sodium carbonate solution.'},
    {'sample_name':'BAS-004-AK','sample_type':'base','pH':'13.00','concentration':'0.1000','temperature':'25.00','notes':'NaOH standard. Strong base.'},
    {'sample_name':'BAS-005-AK','sample_type':'base','pH':'9.20','concentration':'0.0250','temperature':'24.50','notes':'Dilute ammonia. Weak base regime.'},
    {'sample_name':'BAS-006-AK','sample_type':'base','pH':'8.30','concentration':'0.0100','temperature':'25.00','notes':'Sodium bicarbonate. Mild base.'},
    {'sample_name':'BAS-007-AK','sample_type':'base','pH':'12.00','concentration':'0.2000','temperature':'25.00','notes':'Potassium hydroxide. Concentrated.'},
    {'sample_name':'BAS-008-AK','sample_type':'base','pH':'10.20','concentration':'0.0500','temperature':'23.00','notes':'Calcium hydroxide saturated solution.'},
    {'sample_name':'BAS-009-AK','sample_type':'base','pH':'7.80','concentration':'0.0050','temperature':'25.00','notes':'Very dilute base. Close to neutral.'},
    {'sample_name':'BAS-010-AK','sample_type':'base','pH':'13.50','concentration':'0.5000','temperature':'25.00','notes':'Concentrated NaOH. Handle with care.'},

    # BUFFERS (8 entries)
    {'sample_name':'BUF-004-AK','sample_type':'buffer','pH':'6.80','concentration':'0.0500','temperature':'25.00','notes':'Phosphate buffer. Near-neutral range.'},
    {'sample_name':'BUF-005-AK','sample_type':'buffer','pH':'5.00','concentration':'0.1000','temperature':'25.00','notes':'Acetate buffer low range.'},
    {'sample_name':'BUF-006-AK','sample_type':'buffer','pH':'8.00','concentration':'0.0500','temperature':'25.00','notes':'Tris buffer. Biological applications.'},
    {'sample_name':'BUF-007-AK','sample_type':'buffer','pH':'9.00','concentration':'0.0500','temperature':'24.00','notes':'Borate buffer high range.'},
    {'sample_name':'BUF-008-AK','sample_type':'buffer','pH':'6.00','concentration':'0.2000','temperature':'25.00','notes':'MES buffer. Cell culture use.'},
    {'sample_name':'BUF-009-AK','sample_type':'buffer','pH':'7.40','concentration':'0.1000','temperature':'37.00','notes':'PBS at physiological temp. Body temperature run.'},
    {'sample_name':'BUF-010-AK','sample_type':'buffer','pH':'4.50','concentration':'0.0500','temperature':'25.00','notes':'Citrate buffer. Low pH zone.'},
    {'sample_name':'BUF-011-AK','sample_type':'buffer','pH':'8.80','concentration':'0.0750','temperature':'25.00','notes':'HEPES buffer. Biochemistry standard.'},

    # NEUTRAL (4 entries)
    {'sample_name':'NEU-002-AK','sample_type':'neutral','pH':'7.10','concentration':'0.0005','temperature':'25.00','notes':'Deionised water. Freshly prepared.'},
    {'sample_name':'NEU-003-AK','sample_type':'neutral','pH':'6.90','concentration':'0.0010','temperature':'22.00','notes':'Tap water sample. Room temp lower today.'},
    {'sample_name':'NEU-004-AK','sample_type':'neutral','pH':'7.30','concentration':'0.0008','temperature':'25.00','notes':'HPLC-grade water. Reference standard.'},
    {'sample_name':'NEU-005-AK','sample_type':'neutral','pH':'7.00','concentration':'0.0001','temperature':'25.00','notes':'Ultrapure water. Conductivity verified.'},

    # UNKNOWN (4 entries)
    {'sample_name':'UNK-002-AK','sample_type':'unknown','pH':'3.80','concentration':'0.0300','temperature':None,'notes':'From unlabelled storage bottle. Smells acidic.'},
    {'sample_name':'UNK-003-AK','sample_type':'unknown','pH':'9.50','concentration':'0.0150','temperature':'25.00','notes':'Unknown base-like sample. Sent for identification.'},
    {'sample_name':'UNK-004-AK','sample_type':'unknown','pH':'6.40','concentration':'0.0200','temperature':None,'notes':'Slightly acidic. Source unknown.'},
    {'sample_name':'UNK-005-AK','sample_type':'unknown','pH':'11.20','concentration':'0.0500','temperature':'25.00','notes':'High pH unknown. Could be cleaning agent contamination.'},
]

created = 0
for entry in entries:
    exists = ChemicalSample.objects.filter(sample_name=entry['sample_name']).exists()
    if exists:
        print(f"  Skipped (exists): {entry['sample_name']}")
        continue
    obj = ChemicalSample.objects.create(**entry)
    print(f"  Created: {obj}")
    created += 1

print(f"\nDone. {created} new record(s) added. Total in DB: {ChemicalSample.objects.count()}")