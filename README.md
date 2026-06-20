Parking Impact Intelligence System
Problem Statement

Illegal and spillover parking near commercial areas, metro stations, and high-traffic corridors causes congestion and reduces road capacity. Enforcement is often reactive and lacks data-driven prioritization.

Solution

Parking Impact Intelligence System is an AI-driven decision support platform that:

Detects parking congestion hotspots
Predicts future violation-prone locations
Identifies repeat offenders
Calculates an Enforcement Priority Index (EPI)
Generates enforcement recommendations
Visualizes city-wide risk using geospatial analytics
Dataset
298,450 parking violation records
54 police stations
169 junctions
10,942 locations
Key Features
1. Violation Heatmap

Identifies historical parking violation concentration zones.

2. Risk Map

Ranks hotspots using the proposed Enforcement Priority Index (EPI).

3. Forecasting Engine

Predicts future parking violation hotspots using CatBoost Regression.

4. Risk Classification

Classifies locations into Low, Medium, and High risk categories.

5. Repeat Offender Detection

Identifies frequently violating vehicles.

6. Enforcement Planner

Provides actionable deployment recommendations for traffic police.

Machine Learning Models
Forecasting Model
Algorithm: CatBoost Regressor
MAE: 9.49
Risk Classification Model
Algorithm: CatBoost Classifier
Accuracy: 81.8%
Dashboard

The Streamlit dashboard includes:

Overview
Heatmap
Risk Map
EPI Hotspots
Forecasting
Repeat Offenders
Enforcement Planner