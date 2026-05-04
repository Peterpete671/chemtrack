"""
Extracts 5 chemical insights from chemtrack_data.csv
Run after export_data.py
Each insights answers a question from a chemist's perspective
"""

import pandas as pd
import numpy as np

df = pd.read_csv('chemtrack_data.csv')
df['pH'] = pd.to_numeric(df['pH'])
df['concentration'] = pd.to_numeric(df['concentration'])
df['temperature'] = pd.to_numeric(df['temperature'])

print("=" * 60)
print("CHEM-TRACK -- ANALYSIS")
print("=" * 60)

#Insight 1: Average pH per sample type
#Are the samples behaving as expected on average?
#Acid average above 7 is a rd flag - either wrong type label or bad reading

print("\n[1] Average pH by Sample Type")
print("-" * 40)
avg_ph = df.groupby('sample_type')['pH'].agg(['mean', 'min', 'max', 'count'])
avg_ph.columns = ['avg_pH', 'min_pH', 'max_pH', 'count']
print(avg_ph.round(2).to_string())

#INSIGHT 2: Extreme pH values
#Which sample is the most acidic? Most basic?
#These define the measurement boundaries of the entire dataset

print("\n[2] Extreme pH Values")
print("-" * 40)
most_acidic = df.loc[df['pH'].idxmin()]
most_basic = df.loc[df['pH'].idxmax()]
print(f"Most acidic: {most_acidic['sample_name']} | pH {most_acidic['pH']} | {most_acidic['sample_type']}")
print(f"Most basic: {most_basic['sample_name']} | pH {most_basic['pH']} | {most_basic['sample_type']}")

#INSIGHT 3: Concentration distribution
#Are samples spread across a realistic concentration range?
#Clustering near one value suggests limited experimental variety
print("\n[3] Concentration Distribution (mol/L)")
print("-" * 40)
print(df['concentration'].describe().round(4).to_string())
high_conc = df[df['concentration'] > 0.3]
print(f"\nSamples above 0.3 mol/L: {len(high_conc)}")
if len(high_conc) > 0:
    cols = ['sample_name', 'sample_type', 'pH', 'concentration']
    print(high_conc[cols].to_string(index=False))

#INSIGHT 4: pH Consistency Per Type
#Standard deviation measuews how consistent measurements are.
#High std within a single type = recording errors or mixed samples
#A buffer dataset with stdev > 2.0 should raise questions

print("\n[4] pH Consistency (Standard Deviation per Type)")
print("-"* 40)
ph_std = df.groupby('sample_type')['pH'].std().round(3)
print(ph_std.to_string())
print("\n < 1.0 = consistent | > 2.0 = high variability, review needed")

#INSIGHT 5: Temperature deviation flag
#pH changes with temperature. Samples measured away from 25C standard may need correction before comparison.
#Particularly relevant for buffers - phosphate buffer pH shifts - 0.003 units per degree Celcius
print("|n[5] Temperature Deviation from Standard (25C)")
print("-" * 40)
df_temp = df.dropna(subset=["temperature"])
non_std = df_temp[abs(df_temp['temperature'] - 25.0) > 2.0]
std = df_temp[abs(df_temp['temperature'] - 25.0) <= 2.0]
missing = len(df) - len(df_temp)
print(f"At standard temp (25C +/- 2): {len(std)}")
print(f"At non_standard temperature: {len(non_std)}")
print(f"Temperature not recorded: {missing} (assumed 25C)")

if len(non_std) > 0:
    cols = ['sample_name', 'sample_type', 'pH', 'temperature']
    print(["\nNon-standard temperature samples:"])
    print(non_std[cols].to_string(index=False))

print("\n" + "=" * 60)
print(f"Dataset: {len(df)} records | {df['sample_type'].nunique()} sample types")
print("=" * 60)