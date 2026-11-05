
# 🌍 Exoplanet Habitability Explorer

An interactive Python-based project for exploring exoplanets, estimating their habitable zones, screening potentially interesting planetary candidates, and visualizing results through a Streamlit dashboard.

This project uses data from NASA's Exoplanet Archive and combines scientific data analysis, habitable-zone calculations, machine-learning experiments, and interactive visualization.

## 🎯 Project Objectives

- Explore and analyze real exoplanet data.
- Estimate stellar luminosity using stellar radius and effective temperature.
- Calculate conservative and optimistic habitable-zone boundaries.
- Screen small-radius planets located within estimated habitable zones.
- Compare different habitable-zone classification approaches.
- Experiment with machine learning to classify simplified potential-habitability screening labels.
- Build an interactive dashboard to explore planetary candidates.

## 📡 Data Source

This project uses the **NASA Exoplanet Archive – Planetary Systems Composite Parameters (PSCompPars)** dataset.

- Source: https://exoplanetarchive.ipac.caltech.edu/
- Original dataset: `data/raw/exoplanets.csv`

The dataset contains planetary and stellar parameters, including:

- Planet radius
- Orbital period
- Orbital distance
- Planetary insolation flux
- Equilibrium temperature
- Stellar temperature
- Stellar radius
- Stellar mass
- Stellar metallicity

## ⚙️ Methodology

### 1. Data Processing

- Selected relevant planetary and stellar features.
- Examined missing values and data distributions.
- Prepared datasets for exploratory analysis and machine-learning experiments.
- Investigated differences in planetary equilibrium temperatures across discovery methods.

### 2. Stellar Luminosity Estimation

Stellar luminosity is estimated using stellar radius and effective temperature:

\[
\frac{L}{L_\odot} =
\left(\frac{R}{R_\odot}\right)^2
\left(\frac{T}{5772}\right)^4
\]

Where:

- \(L\) = estimated stellar luminosity
- \(R\) = stellar radius
- \(T\) = stellar effective temperature

### 3. Habitable Zone Estimation

The project implements two approaches.

**Fixed-flux model**

Uses simplified inner and outer flux limits of 1.5 and 0.35 Earth insolation units.

**Kopparapu model**

Uses temperature-dependent habitable-zone boundaries based on published coefficients from Kopparapu et al. (2014).

The model estimates:

- Recent Venus boundary
- Runaway greenhouse boundary
- Maximum greenhouse boundary
- Early Mars boundary

These boundaries are used to estimate conservative and optimistic habitable zones.

### 4. Candidate Screening

Planets are classified into four categories:

- Conservative habitable-zone candidates
- Optimistic-only candidates
- Outside the optimistic habitable zone
- Insufficient data

A radius threshold of 1.6 Earth radii is additionally used to identify smaller planets for further screening.

### 5. Machine Learning Experiments

The project includes experiments using:

- Random Forest
- XGBoost
- SHAP-based feature importance
- Classification threshold analysis
- Host-star leakage investigation
- StratifiedGroupKFold cross-validation

#### Label Definition

The machine-learning experiment uses a simplified rule-based screening label:

- Planet radius ≤ 1.6 Earth radii
- Insolation flux between 0.35 and 1.5 Earth units

These rules generate training labels. They are not confirmed scientific habitability labels.

#### Group-Aware Evaluation Results

To reduce host-star information leakage, the project uses StratifiedGroupKFold cross-validation, keeping planets from the same host star together within each fold.

| Metric | Result |
|---|---:|
| Positive examples | 28 |
| Precision | 0.38 |
| Recall | 0.32 |
| F1-score | 0.35 |
| Balanced accuracy | 0.659 |
| True positives detected | 9 / 28 |

The small number of positive examples makes these results uncertain and potentially unstable.

**Important:** The model predicts a simplified rule-based screening label, not actual planetary habitability. Its performance should be treated as an experimental baseline.

## 📊 Streamlit Dashboard

The project includes an interactive dashboard built using Streamlit.

Dashboard features:

- Explore screened planetary candidates.
- Filter planets by habitable-zone category.
- Search for individual planets.
- Filter by planetary radius.
- Visualize habitable-zone classification distributions.
- Explore planetary radius distributions.
- Compare two planets using selected physical parameters.
- Inspect the estimated habitable-zone boundaries of an individual planet.
- Visualize a planet's orbital position relative to its estimated habitable zone.

## 🖥️ Installation and Usage

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/exoplanet-habitability-explorer.git
cd exoplanet-habitability-explorer
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the dashboard

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser, usually at:

```text
http://localhost:8501
```

## 📁 Project Structure

```text
exoplanet-habitability-explorer/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   │   └── exoplanets.csv
│   │
│   └── processed/
│       ├── cleaned_exoplanets.csv
│       ├── final_candidate_summary.csv
│       ├── final_exoplanet_screening.csv
│       └── other_processed_datasets.csv
│
├── src/
│   ├── data/
│   │   └── data processing and habitable-zone scripts
│   │
│   ├── features/
│   │   └── eda.py
│   │
│   ├── models/
│   │   └── machine-learning scripts
│   │
│   └── evaluation/
│       └── model evaluation scripts
│
├── reports/
│   └── figures/
│       ├── planet_radius.png
│       ├── planet_temperature.png
│       ├── radius_vs_temperature.png
│       └── shap_summary.png
│
└── results/
    ├── feature_importance.csv
    └── final_model_results.csv
```

## ⚠️ Scientific Limitations

The results of this project must be interpreted carefully.

1. **Habitable zone does not mean habitable:** A planet inside an estimated habitable zone is not necessarily capable of supporting life.

2. **Atmospheric data:** The current screening pipeline does not establish atmospheric composition, pressure, or surface liquid-water conditions.

3. **Estimated luminosity:** Stellar luminosity is calculated from stellar radius and effective temperature rather than taken as a direct measurement for every star.

4. **Model assumptions:** The Kopparapu calculations use a 1-Earth-mass coefficient set and are restricted to a specified stellar-temperature range.

5. **Orbital eccentricity:** The current orbital screening uses semi-major axis and does not fully model the effects of orbital eccentricity.

6. **Planetary radius:** A radius threshold of 1.6 Earth radii is a screening assumption, not proof that a planet has a rocky composition.

7. **Equilibrium temperature:** Equilibrium temperature is not the same as planetary surface temperature.

8. **Machine-learning labels:** The ML labels are generated from simplified physical-parameter thresholds and do not represent confirmed habitability.

9. **Dataset consistency:** NASA composite parameters can combine measurements from different literature sources and may not always be internally self-consistent.

## 🔬 Future Improvements

- Incorporate atmospheric and planetary composition information when reliable data are available.
- Improve candidate ranking using additional physical parameters.
- Investigate uncertainty in stellar and planetary measurements.
- Explore more robust validation strategies for machine-learning models.
- Add interactive plots and more detailed planetary comparisons.
- Improve data updating and reproducibility.

## 📚 References

- NASA Exoplanet Archive: https://exoplanetarchive.ipac.caltech.edu/
- Kopparapu et al. (2014), *Habitable Zones Around Main-Sequence Stars: New Estimates*: https://doi.org/10.1088/0004-637X/787/2/29

## 👨‍💻 Built With

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- XGBoost
- SHAP
- Streamlit

---

**Disclaimer:** This project is an educational and exploratory data-science application. Its classifications are screening estimates and should not be interpreted as confirmation of planetary habitability or evidence of extraterrestrial life.


