from ninja import Schema
from typing import Optional
from datetime import datetime
class CreateSchema(Schema):
    name:str
    gstin:Optional[str]=None
    sector:Optional[str]='General'
    pan:Optional[str]=None
    address:Optional[str]=None

class UploadSchema(Schema):
    name:str
    file_name:str
    file_type:Optional[str]=None

class UploadResp(Schema):
    presigned_url:str
    file_key:str

class HistoryInpSchema(Schema):
    name:str
    
class HistorySchema(Schema):
    timestamp:datetime
    cam_content:Optional[str]=None
    status:str
    input_file_key:str
    cam_file_key:str
    name:str
    file_url:Optional[str]=None
    handled_by:Optional[str]=None
    uploaded_url:str

class ResearchSchema(Schema):
    name:str
    job_id:str
    qualitative_notes:str

class ExtractSchema(Schema):
    name:str
    input_file_key:str
    file_name:str
    file_type:Optional[str]=None

class CamSchema(Schema):
    job_id:str


    

