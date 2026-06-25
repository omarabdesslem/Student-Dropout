import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

INPUT_FILE  = 'dataset_2022_hash.csv'
OUTPUT_FILE = 'dropout_clean3.csv'

print(f"Reading {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE, sep=';', low_memory=False)
print(f"  Raw shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

print("Fixing decimal commas...")
str_cols = df.select_dtypes(include='object').columns
for col in str_cols:
    converted = df[col].str.replace(',', '.', regex=False)
    as_num = pd.to_numeric(converted, errors='coerce')
    if as_num.notna().sum() > len(df) * 0.1:
        df[col] = as_num

df['dropout_flag'] = (df['abandono_hash'] == 'A').astype(int)

months = [
    '2022_9','2022_10','2022_11','2022_12',
    '2023_1','2023_2','2023_3','2023_4','2023_5','2023_6','2023_7'
]

engagement_metrics = ['pft_days_logged','pft_events','pft_total_minutes',
                      'pft_visits','n_wifi_days','n_resource_days',
                      'pft_assignment_submissions','pft_test_submissions']

for metric in engagement_metrics:
    cols = [f'{metric}_{m}' for m in months if f'{metric}_{m}' in df.columns]
    if cols:
        df[f'total_{metric}'] = df[cols].apply(
            pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)

keep_cols = [
    'dni_hash',
    'tit_hash',               
    'abandono_hash',          
    'dropout_flag',           
    'dedicacion',             
    'anyo_ingreso',           
    'tipo_ingreso',          
    'matricula_activa',      
    'desplazado_hash',       
    'es_retitulado',          
    'rendimiento_total',      
    'rendimiento_cuat_a',     
    'rendimiento_cuat_b',     
    'rend_total_ultimo',      
    'rend_total_penultimo', 
    'cred_mat_total',         
    'cred_sup_total',         
    'cred_sup_normal',        
    'cred_sup_sem_a',         
    'cred_sup_sem_b',         
    'cred_ptes_acta',         
    'curso_mas_bajo',       
    'curso_mas_alto',        
    'impagado_curso_mat',     
    'total_pft_days_logged',
    'total_pft_events',
    'total_pft_total_minutes',
    'total_pft_visits',
    'total_n_wifi_days',
    'total_n_resource_days',
    'total_pft_assignment_submissions',
    'total_pft_test_submissions',
]

keep_cols = [c for c in keep_cols if c in df.columns]
df = df[keep_cols]

print("Deduplicating to one row per student...")

agg = {'dropout_flag': 'max', 'abandono_hash': 'first'}

for col in keep_cols:
    if col not in ('dni_hash', 'dropout_flag', 'abandono_hash'):
        agg[col] = 'first'

df_clean = df.groupby('dni_hash').agg(agg).reset_index()

rename_map = {
    'dni_hash':                        'Student ID',
    'tit_hash':                        'Degree Code',
    'abandono_hash':                   'Status (A=Dropout B=Stayed)',
    'dropout_flag':                    'Dropout (1=Yes 0=No)',
    'dedicacion':                      'Study Mode',
    'anyo_ingreso':                    'Entry Year',
    'tipo_ingreso':                    'Admission Type',
    'matricula_activa':                'Active Enrollment',
    'desplazado_hash':                 'Displaced Student',
    'es_retitulado':                   'Second Degree Student',
    'rendimiento_total':               'Overall Pass Rate (%)',
    'rendimiento_cuat_a':              'Pass Rate Semester A (%)',
    'rendimiento_cuat_b':              'Pass Rate Semester B (%)',
    'rend_total_ultimo':               'Pass Rate Last Year (%)',
    'rend_total_penultimo':            'Pass Rate 2 Years Ago (%)',
    'cred_mat_total':                  'Credits Enrolled Total',
    'cred_sup_total':                  'Credits Passed Total',
    'cred_sup_normal':                 'Credits Passed Normal',
    'cred_sup_sem_a':                  'Credits Passed Sem A',
    'cred_sup_sem_b':                  'Credits Passed Sem B',
    'cred_ptes_acta':                  'Credits Pending Grade',
    'curso_mas_bajo':                  'Lowest Year of Study',
    'curso_mas_alto':                  'Highest Year of Study',
    'impagado_curso_mat':              'Unpaid Fees Flag',
    'total_pft_days_logged':           'Poliformat Days Logged (Total)',
    'total_pft_events':                'Poliformat Events (Total)',
    'total_pft_total_minutes':         'Poliformat Minutes (Total)',
    'total_pft_visits':                'Poliformat Visits (Total)',
    'total_n_wifi_days':               'Campus WiFi Days (Total)',
    'total_n_resource_days':           'Resource Access Days (Total)',
    'total_pft_assignment_submissions':'Assignment Submissions (Total)',
    'total_pft_test_submissions':      'Test Submissions (Total)',
}
df_clean = df_clean.rename(columns=rename_map)

df_clean['Study Mode'] = df_clean['Study Mode'].map(
    {'TC': '1', 'TP': '0'}).fillna(df_clean['Study Mode'])

df_clean['Displaced Student'] = df_clean['Displaced Student'].map(
    {'A': '1', 'B': '0'}).fillna(df_clean['Displaced Student'])

df_clean['Status (A=Dropout B=Stayed)'] = df_clean['Status (A=Dropout B=Stayed)'].map(
    {'A': '1', 'B': '0'}).fillna(df_clean['Status (A=Dropout B=Stayed)'])

df_clean['Entry Year'] = pd.to_numeric(
    df_clean['Entry Year'], errors='coerce').astype('Int64')

rend = pd.to_numeric(df_clean['Overall Pass Rate (%)'], errors='coerce')
df_clean['Performance Bucket'] = pd.cut(
    rend,
    bins=[0, 40, 60, 80, 100],
    labels=['0', '1', '2', '3'],
    include_lowest=True
)

plat = pd.to_numeric(df_clean['Poliformat Days Logged (Total)'], errors='coerce')
df_clean['Engagement Level'] = pd.cut(
    plat,
    bins=[-1, 0, 20, 60, 9999],
    labels=['0', '1', '2', '3']
)

mat = pd.to_numeric(df_clean['Credits Enrolled Total'], errors='coerce')
df_clean['Credits Enrolled Band'] = pd.cut(
    mat,
    bins=[0, 30, 60, 90, 9999],
    labels=['0', '1', '2', '3'],
    include_lowest=True
)

df_clean.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')