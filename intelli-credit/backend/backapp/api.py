from ninja import NinjaAPI
import os, uuid, boto3
from dotenv import load_dotenv
from .schema import UploadSchema, UploadResp, HistorySchema
from ninja.errors import HttpError
from .auth import CustomAuth
from .models import History, Company
from django.shortcuts import get_object_or_404
from typing import List
from .utils.s3_gen import generate_url
load_dotenv()
s3 = boto3.client('s3',
    region_name=os.getenv("S3_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
bucket = os.getenv("S3_BUCKET_NAME")
api = NinjaAPI()

@api.post("/upload", response=UploadResp, auth=CustomAuth())
def upload_file(request, payload:UploadSchema):
    company = payload.company
    file_id = str(uuid.uuid4())
    key = f"docs/{company}/{file_id}-{payload.file_name}"
    presigned_url=generate_url(key, 'put_object')
    return {"presigned_url": presigned_url, "file_key": key}

@api.get("/history", auth=CustomAuth(), response=List[HistorySchema])
def histo(request):
    email=request.auth
    if not email:
        raise HttpError(404, "Company not found")
    company=get_object_or_404(Company, email=email)
    history=History.objects.filter(company=company).order_by("-timestamp")[:50]
    return [{"timestamp": h.timestamp, "cam_content": h.cam_content, "file_key": h.file_key, email:h.company.email, "file_url": generate_url(h.file_key, 'get_object')} for h in history] 
        

    



