# CareerLens Source Code Guide

This folder contains the Python modules used by CareerLens, along with model training, evaluation, testing and data analysis scripts.

## 1. Core API Modules

These are the main modules used by app.py:

| File | Purpose |
|---|---|
| resume_parser.py | Extracts text from PDF and DOCX resumes |
| predict_career_family.py | Predicts career family |
| predict_roles.py | Original trained job-role predictions |
| developer_role_matcher.py | Matches resumes with developer roles using skills and keywords |
| skill_extractor.py | Extracts technical skills |
| skill_gap_analysis.py | Identifies missing skills |
| learning_resource_recommender.py | Recommends learning resources |
| interview_question_generator.py | Generates interview questions |

## 2. Application Workflow

1. User uploads a resume.
2. Resume text is extracted.
3. Career family and job roles are predicted.
4. Developer-role matches are generated.
5. Technical skills are extracted.
6. Skill gaps are analysed.
7. Learning resources and interview questions are generated.
8. Results are returned through the FastAPI application.

## 3. Training and Evaluation Scripts

Scripts such as train_model.py, train_role_model.py, train_career_family_model.py, evaluate_model.py and compare_models.py are used for training and evaluating models.

These scripts are not required to run the existing API.

## 4. Data Analysis Scripts

Scripts beginning with ameo_, analyze_, check_, inspect_ and prepare_ are supporting scripts for dataset analysis, preparation and experiments.

## 5. Testing Scripts

Files beginning with test_ contain tests for individual project modules.

## 6. Important Notes

- Start the application using app.py from the project root.
- Do not run every Python file individually.
- Trained model files are stored in the root models folder.
- Developer role matching is evidence-based and is not a separate trained ML classifier.
- API documentation is available at http://127.0.0.1:8000/docs after starting the server.
