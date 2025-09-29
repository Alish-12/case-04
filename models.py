from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator

#new
import hashlib

class SurveySubmission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    consent: bool = Field(..., description="Must be true to accept")
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = Field(None, max_length=1000)

    #new
    user_agent: Optional[str] = Field(None, description="Browser or client identifier")
    submission_id: Optional[str] = Field(None, description="Unique submission identifier")

    @validator("comments")
    def _strip_comments(cls, v):
        return v.strip() if isinstance(v, str) else v

    @validator("consent")
    def _must_consent(cls, v):
        if v is not True:
            raise ValueError("consent must be true")
        return v
    
    #new
    def hashed(self):
        """Return a version of the model with hashed email and age."""
        data = self.dict()
        data["email"] = hashlib.sha256(data["email"].encode()).hexdigest()
        data["age"] = hashlib.sha256(str(data["age"]).encode()).hexdigest()

        # generate submission_id if missing
        if not data.get("submission_id"):
            timestamp = datetime.now().strftime("%Y%m%d%H")
            data["submission_id"] = hashlib.sha256(
                (data["email"] + timestamp).encode()
            ).hexdigest()
        return data
        
#Good example of inheritance
class StoredSurveyRecord(SurveySubmission):
    received_at: datetime
    ip: str
