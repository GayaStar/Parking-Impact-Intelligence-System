# Parking Impact Intelligence System

## Overview

Parking Impact Intelligence System is an AI-powered traffic analytics platform designed to identify parking-induced congestion hotspots, forecast future parking violation risks, prioritize enforcement zones, and support proactive traffic management.

The system leverages historical parking violation data, machine learning models, geospatial analytics, and risk scoring techniques to help traffic authorities deploy resources more effectively and reduce congestion caused by illegal parking.

---

## Problem Statement

Illegal parking and spillover parking near commercial areas, metro stations, hospitals, schools, and busy junctions significantly reduce road capacity and contribute to traffic congestion.

Current enforcement approaches are largely reactive and patrol-based, making it difficult to:

* Identify recurring violation hotspots
* Prioritize enforcement zones
* Predict future congestion risks
* Detect repeat offenders
* Allocate traffic personnel efficiently

---

## Proposed Solution

The proposed system transforms historical parking violation data into actionable intelligence through:

1. Hotspot Detection
2. Geospatial Heatmaps
3. Risk Mapping
4. Parking Violation Forecasting
5. Risk Classification
6. Repeat Offender Detection
7. Enforcement Priority Index (EPI)
8. AI-driven Enforcement Recommendations

---

## Dataset Statistics

* Total Violation Records: 298,450
* Police Stations: 54
* Junctions: 169
* Unique Locations: 10,942
* Date Range: November 2023 – April 2024

---

## System Architecture

Historical Violation Data

↓

Data Cleaning & Feature Engineering

↓

Hotspot Detection

↓

Machine Learning Models

↓

Risk Forecasting

↓

Enforcement Priority Index (EPI)

↓

Recommendation Engine

↓

Interactive Dashboard

---

## Key Features

### 1. Parking Violation Heatmap

Visualizes historical parking violation density across Bangalore and highlights congestion-prone zones.

### 2. Risk Map

Displays high-priority enforcement locations based on the proposed Enforcement Priority Index (EPI).

### 3. Hotspot Detection

Identifies locations with recurring parking violations and congestion impact.

### 4. Forecasting Engine

Uses CatBoost Regression to predict future parking violation intensity at hotspot locations.

Performance:

* Model: CatBoost Regressor
* Mean Absolute Error (MAE): 9.49

### 5. Risk Classification

Classifies locations into:

* High Risk
* Medium Risk
* Low Risk

Performance:

* Model: CatBoost Classifier
* Accuracy: 81.8%

### 6. Repeat Offender Analysis

Identifies vehicles repeatedly involved in parking violations and supports targeted enforcement actions.

### 7. Enforcement Priority Index (EPI)

A custom scoring mechanism developed to rank hotspots based on:

* Violation Frequency
* Peak Hour Activity
* Repeat Offender Concentration

### 8. Enforcement Planner

Generates actionable recommendations such as:

* Deploy additional officers
* Continuous hotspot monitoring
* Peak-hour patrol scheduling

---

## Technologies Used

### Data Processing

* Python
* Pandas
* NumPy

### Machine Learning

* CatBoost Regressor
* CatBoost Classifier
* Scikit-Learn

### Visualization

* Folium
* Plotly
* Streamlit

### Dashboard

* Streamlit

---

## Dashboard Modules

* Overview
* Parking Violation Heatmap
* Risk Map
* EPI Hotspots
* Violation Forecasting
* Repeat Offenders
* Enforcement Planner

---

## Running the Project

Install dependencies:

pip install -r requirements.txt

Launch the dashboard:

streamlit run app.py

---

## Future Scope

* Integration with real-time parking violation feeds
* CCTV-based parking violation detection
* Dynamic EPI updates
* Automated enforcement alerts
* Smart city traffic management integration

---

## Impact

The proposed solution enables proactive traffic management by predicting parking-induced congestion before it escalates, helping authorities prioritize enforcement actions, improve resource allocation, and reduce traffic disruption in urban environments.