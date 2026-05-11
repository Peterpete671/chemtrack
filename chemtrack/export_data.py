"""
Exports all ChemicalSample records from the database to a CSV file.
Run once before analysis.py
Re-run anytime new records are added to keep the CSV upto date
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemtrack.settings')
django.setup()

import pandas as pd
from samples.models import ChemicalSample

qs = ChemicalSample.objects.all().values(
    'id', 'sample_name', 'sample_type', 'pH',
    'concentration', 'temperature', 'recorded_at'
)

df = pd.DataFrame(list(qs))

if df.empty:
    print("No record found. Add data first.")
    exit()

df['pH'] = pd.to_numeric(df['pH'])
df['concentration'] = pd.to_numeric(df['concentration'])
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
df['recorded_at'] = pd.to_datetime(df['recorded_at'])
df['date'] = df['recorded_at'].dt.date

df.to_csv('chemtrack_data.csv', index=False)
print(f"Exported {len(df)} records to chemtrack_data.csv")
print(f"Sample types: {df['sample_type'].value_counts().to_dict()}")