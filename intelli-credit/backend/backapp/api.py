from ninja import NinjaAPI
import os, uuid, boto3
from dotenv import load_dotenv
from .schema import UploadSchema, UploadResp, HistorySchema, ResearchSchema, ExtractSchema
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
    email = request.auth
    company=get_object_or_404(Company, email=email)
    file_id = str(uuid.uuid4())
    key = f"docs/{company.name}/{file_id}-{payload.file_name}"
    presigned_url=generate_url(key, 'put_object')
    return {"presigned_url": presigned_url, "file_key": key}

@api.get("/history", auth=CustomAuth(), response=List[HistorySchema])
def histo(request):
    email=request.auth
    if not email:
        raise HttpError(404, "Company not found")
    company=get_object_or_404(Company, email=email)
    history=History.objects.filter(company=company).order_by("-timestamp")[:50]
    return [{"timestamp": h.timestamp, "cam_content": h.cam_content, "file_key": h.file_key, "email":h.company.email, "file_url": generate_url(h.file_key, 'get_object')} for h in history] 
        
#TODO: Push job_id, status, gstin, companyName, sector variables,next_topic=research_done to topic=qualitative_notes in pubsub
@api.post("/research", auth=CustomAuth())
def rese(request, payload:ResearchSchema):
    job_id, status=payload.job_id, payload.status
    gstin, companyName= payload.gstin, payload.companyName
    sector= payload.sector
    return None

    

#TODO: Push file key (from frontend), job_id, status, next_topic=extracted-done, bucket name, file_name(from frontend), file_type(from frontend) to topic=extraction-topic in pubsub
@api.post("/extract", auth=CustomAuth())
def extrac(request, payload:ExtractSchema):
    email=request.auth
    company=get_object_or_404(Company, email=email)
    job_id=str(uuid.uuid4())
    History.objects.create(company=company, file_key=payload.file_key, job_id=job_id, status="queued")
    #Push karna baaki hai bhai
    return {"job_id": job_id, "status": "queued"}
    
#TODO: Subscribe to aggregator topic, write to DB



