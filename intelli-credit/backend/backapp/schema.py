from ninja import Schema
from typing import Optional

class UploadSchema(Schema):
    company:str
    sector:Optional[str]='General'
    gstin:Optional[str]=None
    pan:Optional[str]=None
    address:Optional[str]=None
    file_name:str
    content_type:str

class UploadResp(Schema):
    presigned_url:str
    file_key:str
