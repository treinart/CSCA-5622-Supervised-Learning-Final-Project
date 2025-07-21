# CSCA-5622-Supervised-Learning-Final-Project

## Customer Performance Analysis via Regression

This project analyzes and models dealership customer performance using supervised machine learning. The goal is to predict each customer’s average total sales per invoice (labor and parts combined) and understand what factors drive customer value. The analysis uses a fully anonymized, synthetic dataset generated to match real-world business logic and industry KPIs.

---

## Data Privacy and Ethics

**No real customer data is used in this project.**  
The CSV file was programmatically generated using random but realistic values. All company names, customer numbers, and sales figures are fictitious.

---

## Reproducibility

To reproduce this analysis:

1. **Clone the repository:**

git clone https://github.com/treinart/CSCA-5622-Supervised-Learning-Final-Project.git


2. **Install required packages** (see dependencies below).

3. **(Optional) Generate a new dataset:**  
If you wish to create a new anonymized CSV, edit and run `generate_invoice_data.py`.

4. **Run the notebook:**  
Open `final_project.ipynb` in Jupyter Notebook or JupyterLab.  
Make sure `anonymized_invoice_data.csv` is saved in the same folder as the notebook.

5. **Or review the PDFs/reports** for a full walk-through and results.

---

## Project Dependencies and Environment

This notebook requires the following Python packages:

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- scipy
- xgboost

Install missing packages using pip (in a notebook cell or terminal):

pip install pandas numpy matplotlib seaborn scikit-learn scipy xgboost faker


If you see import errors, check your Jupyter kernel matches your Python environment:

import sys
print(sys.executable)

If XGBoost does not install with pip, try:

<full_path_from_above> -m pip install xgboost

Restart your Jupyter kernel after installing.

---

## Usage
Run the notebook (final_project.ipynb) for full exploratory data analysis (EDA), modeling, and business interpretation.

Use generate_invoice_data.py to create fresh, randomized invoice data.

All code and plots are fully reproducible using the attached dataset and script.

---

## Overview of Files
anonymized_invoice_data.csv
Synthetic invoice dataset used for all analysis.
Save this file in the same directory as the Jupyter notebook.
---
final_project.ipynb
Main Jupyter notebook containing all code, analysis, and visualizations.
---
Customer Performance Analysis via Regression.pdf
Final formatted report suitable for submission or review.
---
jupyter_notebook_final_project.pdf
PDF export of the notebook, including code, outputs, and plots.
---
The Story_ Why I Built My Own Data Generator.pdf
A short narrative on the motivation and process behind the custom data generator.
---
generate_invoice_data.py
Python script for generating anonymized, realistic dealership invoice data.
Edit the output path in the script if you wish to generate your own CSV.
---
final_project.html
HTML export of the notebook, viewable in any web browser.
---

## License
This project is licensed under the MIT License.
See LICENSE for full details.

---

## Author
Travis Reinart
travisreinart@gmail.com
University of Colorado Boulder
CSCA 5622: Supervised Learning – Final Project

---

## GitHub Repository
https://github.com/treinart/CSCA-5622-Supervised-Learning-Final-Project

---
