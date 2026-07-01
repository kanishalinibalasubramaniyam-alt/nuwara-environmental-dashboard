# Nuwara Eliya Environmental Data Analysis

## 📋 Project Overview
A complete data analysis project for Nuwara Eliya, Sri Lanka, analyzing climate trends, water quality, and biodiversity data. Includes an interactive dashboard for data visualization.

## 🎯 Skills Demonstrated
- **Python**: Pandas, NumPy, Matplotlib, Seaborn, Scipy
- **SQL**: SQLite database creation and queries
- **Data Cleaning**: Handling missing values, outlier removal
- **Exploratory Data Analysis**: Descriptive statistics, distributions
- **Time Series Analysis**: Trends, seasonality, moving averages
- **Statistical Analysis**: Regression, ANOVA, correlation
- **Data Visualization**: Static and interactive (Plotly/Dash)
- **Dashboard Development**: Interactive web dashboard with filters

## 📊 Key Findings
1. **Temperature**: Warming at +0.01°C/year (statistically significant)
2. **Wind Speed**: Decreasing at -0.03 m/s/year
3. **Water Quality**: Kotagala Wetland (Good), Gregory Lake (Moderate)
4. **Biodiversity**: 12 species recorded, including endemic species

## 📁 Project Structure
nuwara-environmental-dashboard/
├── data/
│ └── nuwara_data.db # SQLite database
├── scripts/
│ ├── database_setup.py # Database creation script
│ └── dashboard.py # Interactive dashboard
├── notebooks/
│ └── analysis.ipynb # Jupyter notebook analysis
├── outputs/ # Generated charts
│ ├── temperature_trend.png
│ ├── water_quality.png
│ ├── biodiversity.png
│ ├── correlation_matrix.png
│ └── insights_recommendations.txt
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore file
└── README.md # This file


## 🚀 How to Run

### 1. Clone the Repository
git clone https://github.com/your-username/nuwara-environmental-dashboard.git
cd nuwara-environmental-dashboard

python -m venv venv
venv\Scripts\activate         # On Windows

pip install -r requirements.txt

cd scripts
python database_setup.py

jupyter notebook
# Open notebooks/analysis.ipynb and run all cells

python dashboard.py
# Open http://127.0.0.1:8050 in your browser
