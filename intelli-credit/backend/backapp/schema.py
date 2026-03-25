from ninja import Schema
from typing import Optional
from datetime import datetime

class UploadSchema(Schema):
    name:str
    file_name:str
    content_type:str

class UploadResp(Schema):
    presigned_url:str
    file_key:str

class HistorySchema(Schema):
    timestamp:datetime
    cam_content:str
    file_key:str
    file_url:str
    email:str

class ResearchSchema(Schema):
    job_id:str
    status:str
    gstin:str
    name:str
    sector:str

class ExtractSchema(Schema):
    name:str
    file_key:str
    job_id:str
    status:str
    file_name:str
    file_type:str

class CreateSchema(Schema):
    name:str
    gstin:Optional[str]=None
    sector:Optional[str]='General'
    pan:Optional[str]=None
    address:Optional[str]=None


class HistoryInpSchema(Schema):
    name:str


