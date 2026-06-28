# ⚽ Football Analytics Pro

A machine learning–powered football player performance prediction system.  
This project implements a complete ML pipeline to analyze historical European football data and predict player performance scores and classes (High, Medium, Low).  

---

## 📌 Project Overview
- **Goal:** Predict football player performance using historical match, player, and team data.  
- **Dataset:** European Soccer Database (Kaggle, 2008–2016).  
- **Tech Stack:** Python, Pandas, NumPy, Scikit‑Learn, XGBoost, LightGBM, CatBoost, Streamlit.  
- **Deployment:** Google Colab + Streamlit dashboard.  

---

## 🏗️ System Architecture
### Frontend
- Built with **Streamlit** for interactive dashboards.  
- Features:
  - Player selection and performance visualization.
  - Predicted performance score (0–100).
  - Classification into High/Medium/Low tiers.
  - Interactive charts and comparison tools.

### Backend
- **Data Processing:** Pandas, NumPy.  
- **ML Models:** Scikit‑Learn, XGBoost, LightGBM, CatBoost.  
- **Balancing:** SMOTE (imblearn).  
- **Persistence:** Pickle for saving trained models.  

### Training Infrastructure
- Developed in **Google Colab** with GPU/TPU acceleration.  
- Integrated with Google Drive for dataset storage, models, and figures.  

---

## 📊 Dataset
- **Source:** [European Soccer Database – Kaggle](https://www.kaggle.com/datasets/hugomathien/soccer)  
- **Tables Used:**
  - `Match.csv` – Match outcomes, goals, season, stage.  
  - `Player.csv` – Player identifiers and biographical data.  
  - `Player_Attributes.csv` – Player skill ratings over time.  
  - `Team.csv` – Team identifiers and names.  
  - `Team_Attributes.csv` – Tactical and strength metrics.  

---

## 🔑 Features
- **Player attributes:** rating, stamina, dribbling, finishing, sprint speed, etc.  
- **Team attributes:** build‑up play, chance creation, defense metrics.  
- **Match context:** goals, stage, home/away, difficulty.  
- **Engineered features:** recent form, team strength index, weighted performance score.  

---

## 🧹 Data Preprocessing
- Missing value imputation (median for numerical attributes).  
- Duplicate removal.  
- Feature scaling (StandardScaler).  
- Encoding categorical variables.  
- Relational joins across player, match, and team tables.  

---

## 🤖 Models
### Regression (Performance Score Prediction)
- **Linear Regression (baseline):** R² = 0.87  
- **XGBoost Regressor:** R² = 0.9730  
- **LightGBM Regressor:** R² = 0.9710  
- **Stacking Ensemble (best):** R² = 0.9731, MAE = 1.67  

### Classification (Performance Tier Prediction)
- **Logistic Regression (baseline):** Accuracy = 0.87  
- **Random Forest Classifier:** Accuracy = 0.92  
- **XGBoost Classifier (best):** Accuracy = 0.94, F1 = 0.94  

---

## 📈 Evaluation
- Metrics: Accuracy, Precision, Recall, F1‑Score, R², MAE, RMSE.  
- Confusion matrix and classification reports for model validation.  
- Visual inspection with rating distributions, feature importance plots, and prediction trends.  

---

## 🚀 Dashboard Features
- Player analytics (filter by rating, age, potential).  
- Compare players head‑to‑head.  
- Top performers ranking.  
- Performance distribution visualization.  
- AI predictor for future match performance.  

---

## ⚡ Challenges
- Large dataset size (memory management in Colab).  
- Missing attributes for some players.  
- Complex relational joins.  
- Feature selection experimentation.  
- Overfitting mitigated with train‑test split and hyperparameter tuning.  

---

## 📚 References
- [European Soccer Database – Kaggle](https://www.kaggle.com/datasets/hugomathien/soccer)  
- [Scikit‑Learn Documentation](https://scikit-learn.org/stable/)  
- [XGBoost Documentation](https://xgboost.readthedocs.io/en/stable/)  
- [Pandas Documentation](https://pandas.pydata.org/docs/)  
- [NumPy Documentation](https://numpy.org/doc/)  
- [Google Colab](https://colab.research.google.com/)  

---
