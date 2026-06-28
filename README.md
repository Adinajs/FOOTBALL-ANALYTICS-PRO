# Football Analytics Pro: Player Performance Prediction System

[cite_start]Football Analytics Pro is an end-to-end data science and machine learning pipeline that automates the predictive assessment of professional football players[cite: 454, 455]. [cite_start]Utilizing historical match data from the European Soccer Database, the platform cleans, structures, and processes multi-table relational inputs to train both regression and classification frameworks[cite: 455, 456, 457]. 

[cite_start]The system maps precise continuous performance scores while grouping players into descriptive behavioral clusters (High, Medium, and Low tier execution thresholds) to replace subjective reporting models with mathematical insight[cite: 457, 463, 465]. [cite_start]The operational features are deployed to users via an interactive web dashboard[cite: 478].

---

## 🚀 Key Features

- [cite_start]**Dual Modeling Framework:** Executes concurrent regression pipelines to calculate detailed performance indices ($0-100$) alongside robust classification boundaries to segment players into dynamic target profiles[cite: 457, 481].
- [cite_start]**Advanced Machine Learning Architectures:** Leverages high-performance ensemble trees, incorporating tuned **XGBoost**, **LightGBM**, and a generalized **Stacking Regressor**[cite: 488, 714, 724].
- [cite_start]**Interactive Analytics Dashboard:** Formulated with Streamlit to enable scouts, managers, and analytical staff to query specific players, review comparative traits, plot physical projections, and measure workload distributions[cite: 478, 479, 480].
- [cite_start]**Relational Data Optimization:** Resolves complex historical structural mismatches by executing strict time-aware backward joins (`pd.merge_asof`) across multiple databases[cite: 672, 676].
- [cite_start]**Tailored PDF Reporting:** Compiles multi-tiered attribute scores, performance forecasts, and baseline biographical breakdowns into standard executive summary sheets downloadable instantly as PDFs[cite: 1344, 1368].

---

## 🏗️ System Architecture

[cite_start]The software setup separates platform operations into isolated backend engineering segments alongside human-accessible visualization frontends[cite: 475, 476]:

1. [cite_start]**User Presentation Layer (Streamlit Dashboard):** Coordinates individual athlete profiling, player head-to-head comparisons, contextual filtering, tactical team health monitors, and automated form tracking metrics[cite: 478, 480, 482].
2. [cite_start]**Computational Logic & Backend Pipelines:** Standardized entirely in Python using foundational data frames (`pandas`, `numpy`)[cite: 486, 487, 488]. [cite_start]Mathematical operations utilize `scikit-learn`, `xgboost`, and `lightgbm` alongside `imblearn` modules to manage dataset alignment[cite: 488, 489].
3. [cite_start]**Storage & GPU Infrastructure:** Hosted through cloud instances with integrated data mounts to isolate physical resource pipelines from file compilation zones[cite: 520, 521, 522].

---

## 📊 Dataset Specifications

- [cite_start]**Source Reference:** Kaggle European Soccer Database[cite: 536].
- [cite_start]**Temporal Bound:** Extensive match records spanning historical metrics from 2008 to 2016[cite: 538].
- **Data Shape Metrics:**
  - [cite_start]`Match.csv`: $25,979$ instances across $115$ feature tracks[cite: 609].
  - [cite_start]`Player.csv`: Biographical identities for $11,060$ individual professionals[cite: 610].
  - [cite_start]`Player_Attributes.csv`: $183,978$ operational rows auditing physical/tactical variations[cite: 611].
  - [cite_start]`Team.csv` & `Team_Attributes.csv`: Ground truth profiles for hundreds of unique club contexts[cite: 612, 613].

### Engineered Metric Targets
[cite_start]The project computes baseline attributes into composite metrics, including[cite: 619]:
- [cite_start]Custom composite indices: `attacking_score`, `defensive_score`, `physical_score`, `technical_score`, `mental_score`[cite: 627].
- [cite_start]Comprehensive rolling status: `recent_form_3`, `recent_form_5`, `recent_form_10`[cite: 635].
- [cite_start]Collective comparative metrics: `strength_difference`, `match_difficulty`, `attack_x_team_strength`[cite: 633, 640].

---

## 🔧 Preprocessing Checklist

- [cite_start]**Datetime Alignment:** Converts mismatched system timestamps to chronological pandas types before performing multi-table merges[cite: 643, 644].
- [cite_start]**Relational Data Join:** Blends physical metrics into tactical team attributes through backward time-tolerant joins clamped strictly inside a $365$-day evaluation window[cite: 672, 676, 681].
- [cite_start]**Missing Value Resolution:** Handles systemic column absence across key parameters via localized median imputation routines to avoid downstream operational failures[cite: 656, 658].
- [cite_start]**Class Balancing:** Addresses target distribution patterns (such as heavily localized Medium class concentrations) through Synthetic Minority Over-sampling Techniques (**SMOTE**)[cite: 489, 740].
- [cite_start]**Standard Scale Transforms:** Standardizes irregular scaling profiles using `StandardScaler` to normalize structural impacts during tree splits[cite: 667].

---

## 📈 Evaluation & Performance Profiles

[cite_start]Data splits use an un-biased $80/20$ division matrix across a working pool of $532,395$ historical matches[cite: 753, 756].

### 1. Regression Framework Results (Performance Index Predictor)
| Architecture Base | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) | R-Squared ($R^2$) Score |
| :--- | :---: | :---: | :---: |
| **Stacking Ensemble (Best Regressor)** | **1.6739** | **2.2053** | [cite_start]**0.9731** | [cite: 730, 731]
| XGBoost Regressor | 1.6804 | 2.2079 | [cite_start]0.9730 | [cite: 730]
| LightGBM Regressor | 1.7521 | 2.2916 | [cite_start]0.9710 | [cite: 730]
| Linear Regression Baseline | 3.9762 | 4.8389 | [cite_start]0.8705 | [cite: 730]

### 2. Classification Framework Results (Performance Tier Identifier)
| Classifier Variant | Test Accuracy Score | Precision Metrics | Recall Metrics | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **XGBoost Classifier (Best Classifier)** | **93.80%** | **0.9392** | **0.9380** | [cite_start]**0.9384** | [cite: 746, 747]
| Random Forest Classifier | 91.88% | 0.9276 | 0.9188 | [cite_start]0.9208 | [cite: 746]
| Logistic Regression Baseline | 87.36% | 0.9016 | 0.8736 | [cite_start]0.8787 | [cite: 746]

---
