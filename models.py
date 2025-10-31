from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile

class StartupRequest(BaseModel):
    startup_name: str
    tagline: str
    description: str
    introduction: str
    sections: List[str]  # sections user wants to include
    generate_logo: bool = False  # whether to generate logo
    # uploaded files are optional
    logo_file: Optional[UploadFile] = None
    profile_picture: Optional[UploadFile] = None
