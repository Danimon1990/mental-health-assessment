from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Dict, Optional, Union
from datetime import datetime
import logging
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase Admin
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    logger.info("Firebase initialized successfully")
except Exception as e:
    logger.error(f"Error initializing Firebase: {str(e)}")
    raise

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define data models
class FormSubmission(BaseModel):
    email: EmailStr
    timestamp: datetime
    result: str
    selectedCheckboxes: Dict[str, Union[Dict[str, List[str]], List[str]]]

    @field_validator('selectedCheckboxes')
    @classmethod
    def validate_checkboxes(cls, v):
        required_keys = ['anxiety', 'panic', 'depression', 'adhd', 'adjustment']
        for key in required_keys:
            if key not in v:
                raise ValueError(f"Missing required key in selectedCheckboxes: {key}")
        return v

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI server!"}

@app.post("/submit-form")
async def submit_form(request: Request):
    try:
        # Get raw request body
        body = await request.body()
        body_str = body.decode('utf-8')
        logger.info(f"Received request body: {body_str}")
        
        # Parse JSON
        form_data = json.loads(body_str)
        
        # Validate data
        submission = FormSubmission(**form_data)
        
        # Convert to dict for Firebase
        submission_dict = submission.dict()
        
        # Store in Firebase
        try:
            # Add a new document with a generated ID
            doc_ref = db.collection('form_submissions').add(submission_dict)
            logger.info(f"Document added with ID: {doc_ref[1].id}")
        except Exception as e:
            logger.error(f"Error storing in Firebase: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error storing data: {str(e)}")
        
        return {
            "status": "success",
            "message": "Form submitted successfully",
            "data": submission_dict
        }
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
