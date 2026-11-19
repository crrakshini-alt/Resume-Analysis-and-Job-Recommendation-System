\# Source Code Guide



This folder contains the Python modules used by CareerLens, along with model training, evaluation, data analysis and testing scripts.



\## 1. Core API Modules



These modules are imported by the main application (`app.py`).



| File | Responsibility |

|---|---|

| `resume\_parser.py` | Extracts text from PDF and DOCX resumes |

| `predict\_career\_family.py` | Predicts the candidate's career family |

| `predict\_roles.py` | Runs the original trained job-role classification model |

| `developer\_role\_matcher.py` | Matches resumes against developer-role profiles using skill and keyword evidence |

| `skill\_extractor.py` | Extracts technical skills |

| `skill\_gap\_analysis.py` | Compares candidate skills with predefined job-role requirements |

| `learning\_resource\_recommender.py` | Recommends learning resources |

| `interview\_question\_generator.py` | Generates interview questions |



\## 2. How the API Works



The main entry point is `app.py` in the project root.



General workflow:



1\. The user uploads a resume through the API.

2\. `resume\_parser.py` extracts the resume text.

3\. Prediction modules analyse career family and job roles.

4\. `developer\_role\_matcher.py` evaluates developer-role matches.

5\. `skill\_extractor.py` identifies technical skills.

6\. `skill\_gap\_analysis.py` identifies missing skills.

7\. Learning resources and interview questions are generated.

8\. The API returns the analysis results.



\## 3. Training and Evaluation Scripts



Files such as:



\- `train\_model.py`

\- `train\_role\_model.py`

\- `train\_role\_model\_v2.py`

\- `train\_career\_family\_model.py`

\- `evaluate\_model.py`

\- `evaluate\_role\_model.py`

\- `compare\_models.py`



These are used for model training, experiments and evaluation. They are not required to start the API when the trained model files are already available.



\## 4. Data Analysis and Utility Scripts



Files beginning with names such as `analyze\_`, `check\_`, `inspect\_`, `prepare\_` and `ameo\_` are supporting scripts for dataset analysis, preparation and experiments.



\## 5. Testing Scripts



Files beginning with `test\_` are used for testing individual modules and functionality.



\## 6. Important Notes



\- Start the application using `app.py` from the project root.

\- Do not run every Python file individually.

\- The trained model files are stored in the root `models/` directory.

\- The developer-role matcher is a rule-based evidence matcher, not a separate trained ML classifier.

\- The frontend can integrate with the FastAPI endpoints documented at `/docs`.

