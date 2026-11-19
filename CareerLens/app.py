
from pathlib import Path
import sys
import tempfile

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware


# Project directory
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "src"))


# Import project modules
from resume_parser import extract_resume_text
from predict_roles import predict_roles, get_all_role_scores
from predict_career_family import predict_career_family
from developer_role_matcher import predict_developer_roles
from skill_extractor import extract_skills
from skill_gap_analysis import JOB_ROLES, analyze_skill_gap
from interview_question_generator import generate_interview_questions


# FastAPI application
app = FastAPI(
    title="CareerLens Resume Analysis API",
    description="AI-based resume analysis and career readiness assessment for freshers",
    version="1.6"
)


# Frontend communication during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = [".pdf", ".docx"]


@app.get("/")
def home():
    return {
        "message": "CareerLens API is running!",
        "version": "1.6"
    }


@app.get("/roles")
def get_roles():
    available_roles = list(JOB_ROLES.keys())

    return {
        "total_roles": len(available_roles),
        "available_roles": available_roles
    }


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    selected_role: str = Form(None)
):

    temp_path = None

    try:

        # 1. Validate filename and extension
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Please upload a resume file."
            )

        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported."
            )

        # 2. Read uploaded file with size limit
        file_bytes = await file.read(MAX_FILE_SIZE + 1)

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File size must not exceed 10 MB."
            )

        # 3. Save file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            temp_file.write(file_bytes)
            temp_path = Path(temp_file.name)

        # 4. Extract resume text
        resume_text = extract_resume_text(temp_path)

        if not resume_text or not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the resume."
            )

        # 5. Predict broad career family
        predicted_career_family = predict_career_family(resume_text)

        # 6. Existing trained IT role predictions
        all_role_scores = get_all_role_scores(resume_text)

        predicted_roles = predict_roles(resume_text)

        if predicted_roles:
            role_prediction_status = (
                "Specific IT roles identified above the trained model threshold."
            )
        else:
            role_prediction_status = (
                "No specific IT role met the trained model threshold. "
                "All existing model scores are available for examination."
            )

        # 7. New expandable developer-role matching
        developer_role_matches = predict_developer_roles(resume_text)

        top_developer_roles = developer_role_matches[:5]

        if developer_role_matches:
            developer_role_matching_status = (
                "Developer roles matched using resume skill and keyword evidence."
            )
        else:
            developer_role_matching_status = (
                "Insufficient developer-role evidence found in the resume."
            )

        # 8. Extract skills
        skills = extract_skills(resume_text)

        # 9. Get available skill-gap analysis roles
        available_roles = list(JOB_ROLES.keys())

        # 10. Validate selected role if provided
        if selected_role and selected_role not in available_roles:
            raise HTTPException(
                status_code=400,
                detail="Invalid job role selected."
            )

        # 11. Compare resume with every available skill-gap role
        all_role_analysis = {}

        for role in available_roles:

            skill_gap = analyze_skill_gap(skills, role)

            required_skills = JOB_ROLES[role]

            role_questions = generate_interview_questions(
                required_skills
            )

            all_role_analysis[role] = {
                "skill_gap_analysis": skill_gap,
                "interview_questions": role_questions
            }

        # 12. Get selected role analysis
        selected_role_analysis = None

        if selected_role:
            selected_role_analysis = all_role_analysis[selected_role]

        # 13. Return analysis results
        return {
            "filename": file.filename,

            "resume_status": "Successfully analyzed",

            "predicted_career_family": predicted_career_family,

            # Existing trained ML model output
            "predicted_roles": predicted_roles,

            "all_role_scores": all_role_scores,

            "role_prediction_status": role_prediction_status,

            # New developer-role matching output
            "developer_role_matches": developer_role_matches,

            "top_developer_roles": top_developer_roles,

            "developer_role_matching_status": (
                developer_role_matching_status
            ),

            # Extracted resume skills
            "extracted_skills": skills,

            # Existing skill-gap analysis
            "total_roles_compared": len(available_roles),

            "all_role_analysis": all_role_analysis,

            "selected_role": selected_role,

            "selected_role_analysis": selected_role_analysis
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        print(f"Resume analysis error: {error}")

        raise HTTPException(
            status_code=500,
            detail=(
                "Resume analysis failed. "
                "Please check the uploaded file and try again."
            )
        )

    finally:

        # 14. Delete temporary file
        if temp_path and temp_path.exists():
            temp_path.unlink()

        await file.close()
