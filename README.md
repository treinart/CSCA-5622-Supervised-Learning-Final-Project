# CSCA-5622-Supervised-Learning-Final-Project
CSCA 5622 Supervised Learning Final Project - Customer Performance Analysis via Regression
Overview
This project analyzes and models dealership customer performance using supervised machine learning. The goal is to predict each customer’s average total sales per invoice (labor and parts combined) and understand what factors drive customer value. The analysis uses a fully anonymized, synthetic dataset generated to match real-world business logic and industry KPIs.

Contents
Customer Performance Analysis via Regression .ipynb – Main Jupyter notebook (analysis, modeling, visualizations, commentary)

Customer Performance Analysis via Regression .pdf – Final written report

generate_invoice_data.py – Python script to generate the anonymized dealership invoice dataset

anonymized_invoice_data.csv – The actual dataset used for all modeling and analysis

Generate Anonymized Data Story.docx – Documentation explaining the design and logic behind the synthetic data generator

Data Privacy and Ethics
No real customer data is used in this project. The CSV file was programmatically generated using random but realistic values. All company names, customer numbers, and sales figures are fictitious.

Reproducibility
To reproduce this analysis:

Clone the repository

git clone https://github.com/treinart/CSCA-5622-Supervised-Learning-Final-Project.git

Install required packages (see below)

Run the data generator (optional):
If you wish to create a new anonymized CSV, edit and run generate_invoice_data.py

Open the Jupyter notebook and run all cells, or review the PDF/report for results.

Required Python Packages
pandas

numpy

matplotlib

seaborn

scikit-learn

scipy

xgboost

faker

Install all with:

pip install pandas numpy matplotlib seaborn scikit-learn scipy xgboost faker

Usage
Review or run the notebook for full exploratory data analysis (EDA), modeling, and business interpretation.

The script generate_invoice_data.py can be run independently to create fresh, randomized invoice data that matches dealership KPIs and business rules.

All plots and code in the notebook are fully reproducible using the attached dataset and script.

License
This project is licensed under the [MIT License](LICENSE).

Author
Travis Reinart
travisreinart@gmail.com
University of Colorado Boulder
CSCA 5622: Supervised Learning – Final Project
