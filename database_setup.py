import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Ensure data directory exists
os.makedirs('../data', exist_ok=True)

# Create database
conn = sqlite3.connect('../data/nuwara_data.db')
cursor = conn.cursor()

# CREATE TABLES
print("Creating tables...")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS climate_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        temperature REAL,
        humidity REAL,
        rainfall REAL,
        wind_speed REAL,
        pressure REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS water_quality (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT NOT NULL,
        date TEXT NOT NULL,
        ph REAL,
        dissolved_oxygen REAL,
        turbidity REAL,
        nitrate REAL,
        water_quality_index REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS biodiversity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT NOT NULL,
        species TEXT NOT NULL,
        category TEXT,
        endemic INTEGER,
        count INTEGER,
        date TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        report_type TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )
''')

print("Tables created successfully")

# GENERATE CLIMATE DATA
print("Generating climate data (1990-2026)...")

np.random.seed(42)
dates = pd.date_range('1990-01-01', '2026-06-01', freq='ME')  # Changed 'M' to 'ME'
n = len(dates)

climate_data = pd.DataFrame({
    'date': dates.strftime('%Y-%m-%d'),
    'temperature': 15.5 + 0.01 * np.arange(n) + np.random.normal(0, 1.5, n),
    'humidity': 78 + 0.02 * np.arange(n) + np.random.normal(0, 5, n),
    'rainfall': 150 + 0.5 * np.sin(np.arange(n)/12*2*np.pi) + np.random.normal(0, 40, n),
    'wind_speed': 3.5 - 0.03 * np.arange(n)/12 + np.random.normal(0, 0.8, n),
    'pressure': 1010 + np.random.normal(0, 5, n)
})

climate_data['temperature'] = climate_data['temperature'].clip(8, 25)
climate_data['humidity'] = climate_data['humidity'].clip(60, 100)
climate_data['rainfall'] = climate_data['rainfall'].clip(20, 400)
climate_data['wind_speed'] = climate_data['wind_speed'].clip(1, 8)
climate_data['pressure'] = climate_data['pressure'].clip(1000, 1025)

climate_data.to_sql('climate_data', conn, if_exists='replace', index=False)
print(f"Climate records generated: {len(climate_data)}")

# GENERATE WATER QUALITY DATA
print("Generating water quality data...")

sites = ['Victoria Park', 'Gregory Lake', 'Kotagala Wetland', 'Horton Plains', "Galway's Land"]
site_quality = {'Victoria Park': 85, 'Gregory Lake': 62, 'Kotagala Wetland': 88, 
                'Horton Plains': 78, "Galway's Land": 72}

wq_data = []
for site in sites:
    for i in range(24):
        date = (datetime.now() - timedelta(days=i*30)).strftime('%Y-%m-%d')
        base = site_quality[site]
        wq_data.append({
            'site': site,
            'date': date,
            'ph': np.random.normal(7.0, 0.5),
            'dissolved_oxygen': np.random.normal(8.0, 1.0),
            'turbidity': np.random.normal(5.0, 2.0),
            'nitrate': np.random.normal(2.0, 0.8),
            'water_quality_index': base + np.random.normal(0, 5)
        })

wq_df = pd.DataFrame(wq_data)
wq_df['water_quality_index'] = wq_df['water_quality_index'].clip(30, 100)
wq_df.to_sql('water_quality', conn, if_exists='replace', index=False)
print(f"Water quality records generated: {len(wq_df)}")

# GENERATE BIODIVERSITY DATA
print("Generating biodiversity data...")

species_data = [
    ('Victoria Park', 'Indian Blue Robin', 'Bird', 1, 45),
    ('Victoria Park', 'Kashmir Flycatcher', 'Bird', 0, 20),
    ('Victoria Park', 'Pied Thrush', 'Bird', 0, 15),
    ("Galway's Land", 'Barking Deer', 'Mammal', 1, 15),
    ("Galway's Land", 'Wild Boar', 'Mammal', 0, 25),
    ("Galway's Land", 'Purple-faced Langur', 'Mammal', 1, 30),
    ('Horton Plains', 'Leopard', 'Mammal', 0, 8),
    ('Horton Plains', 'Sambar', 'Mammal', 0, 30),
    ('Horton Plains', 'Dull-blue Flycatcher', 'Bird', 1, 25),
    ('Kotagala Wetland', 'Endemic Butterfly', 'Insect', 1, 60),
    ('Kotagala Wetland', 'Sri Lanka White-eye', 'Bird', 1, 40),
    ('Kotagala Wetland', 'Yellow-eared Bulbul', 'Bird', 1, 35),
]

biodiv_data = []
for site, species, category, endemic, count in species_data:
    for i in range(4):
        date = (datetime.now() - timedelta(days=i*90)).strftime('%Y-%m-%d')
        variation = np.random.normal(1.0, 0.15)
        biodiv_data.append({
            'site': site,
            'species': species,
            'category': category,
            'endemic': endemic,
            'count': max(1, int(count * variation)),
            'date': date
        })

biodiv_df = pd.DataFrame(biodiv_data)
biodiv_df.to_sql('biodiversity', conn, if_exists='replace', index=False)
print(f"Biodiversity records generated: {len(biodiv_df)}")

# GENERATE REPORTS DATA
print("Generating sample reports...")

sample_reports = [
    ('Victoria Park', 'Wildlife Sighting', 'Saw Indian Blue Robin near entrance', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ('Gregory Lake', 'Water Quality', 'Green algae spotted near boating area', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ('Kotagala Wetland', 'Litter/Waste', 'Plastic bottles found near walking trail', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ('Horton Plains', 'Other', 'Mist clearing late, visibility poor', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
]

for location, report_type, description, date in sample_reports:
    cursor.execute('''
        INSERT INTO reports (location, report_type, description, date)
        VALUES (?, ?, ?, ?)
    ''', (location, report_type, description, date))

conn.commit()
print(f"Sample reports added: {len(sample_reports)}")

# VERIFY DATA
print("\n" + "="*50)
print("DATABASE SUMMARY")
print("="*50)

tables = ['climate_data', 'water_quality', 'biodiversity', 'reports']
for table in tables:
    count = cursor.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
    print(f"Table: {table}, Records: {count}")

conn.close()
print("\nDatabase setup complete")
print("Location: ../data/nuwara_data.db")