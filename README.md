# Student Dropout Prediction

Git repository for the **Student Dropout Project**, developed as part of the **UPV / PW / ETH Zürich / Politecnico Milano** collaboration.

The project explores how academic performance and student engagement data can be used to identify students who may be at risk of dropping out.

## Project Overview

High dropout rates in STEM programmes affect:

* Students
* Universities
* National education systems

This project proposes an early-warning algorithm that evaluates students’ academic performance and campus engagement to estimate their likelihood of dropping out.

The objective is to help universities take pre-emptive action and provide support to students earlier.

## Project Goals

* Identify students who may be at risk of dropping out.
* Analyse the relationship between academic performance, engagement, and dropout.
* Compare different prediction methods.
* Support earlier intervention by universities.
* Provide statistical insights into dropout patterns.

## Methodology

The project follows four main stages:

1. Data cleaning
2. Feature engineering and clustering
3. Correlation analysis
4. Model training and evaluation

## Data Preparation

### Row Reduction

The original dataset was reduced through de-duplication and filtering:

| Processing stage      | Number of rows |
| --------------------- | -------------: |
| Raw dataset           |        159,174 |
| After de-duplication  |         20,428 |
| Final trimmed dataset |          9,185 |

### Column Reduction

The number of variables was also reduced:

| Processing stage        | Number of columns |
| ----------------------- | ----------------: |
| Raw dataset             |               169 |
| Cleaned dataset         |                33 |
| Final selected features |                12 |

Categorical variables were converted into binary or model-compatible values.

## Feature Engineering

Several variables were created or grouped to improve the analysis:

* Academic performance buckets
* PoliformaT engagement
* Total enrolled credits
* Previous-semester academic results
* Completed-credit indicators

The performance buckets group students into ranges such as:

* 0–40%
* 40–60%
* 60–80%
* 80–100%

## Correlation Analysis

Pearson correlation was calculated between each selected feature and the dropout variable.

Statistical significance was also evaluated to determine whether the observed relationships were meaningful.

The analysis indicated that academic performance and previously completed credits were among the variables associated with dropout behaviour.

## Prediction Models

The project explored several predictive approaches:

* Linear Regression
* Gradient Descent
* Logistic Regression
* Gradient Boosting
* XGBoost
* Classification Tree
* Random Forest
* Custom prediction algorithm

## Initial Results

The presentation reports the following results for the two initial approaches:

| Model             | Accuracy | Precision | Recall |
| ----------------- | -------: | --------: | -----: |
| Gradient Descent  |    0.741 |     0.083 |  0.638 |
| Linear Regression |    0.962 |     0.405 |  0.188 |

### Interpretation

The models demonstrate an important trade-off:

* **Linear Regression** achieved higher overall accuracy and precision.
* **Gradient Descent** identified a larger proportion of dropout cases, resulting in higher recall.

For an early-warning system, recall is particularly important because a false negative represents an at-risk student who was not identified.

However, accuracy should not be considered independently because the dataset contains considerably fewer dropout cases than non-dropout cases.

## Suggested Workflow

Planned improvements include:

* Testing additional machine-learning models.
* Exploring new academic and engagement features.
* Adding exogenous data.
* Improving the detection of minority dropout cases.
* Addressing class imbalance.
* Performing additional model validation.
* Evaluating the model across different universities and programmes.

## Responsible Use

This project should be used as a decision-support tool rather than as an automated decision-making system.

A dropout-risk prediction should trigger supportive actions, such as academic guidance or student outreach. It should not be used to penalise students or restrict access to university services.

Student information must be processed securely and in accordance with applicable privacy and data-protection requirements.

## Team Cloud

* Omar Abdesslem
* Gergely Maros
* Szymon Predel
* Vincent Dharma Satria

## Institutions

* Universitat Politècnica de València — UPV
* Warsaw University of Technology — PW

## License

Add the selected project license here, for example:

```text
MIT License
```
