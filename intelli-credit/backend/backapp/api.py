from ninja import NinjaAPI
import os, uuid, boto3
from dotenv import load_dotenv
from .schema import UploadSchema, UploadResp, HistorySchema, ResearchSchema, ExtractSchema, CreateSchema, HistoryInpSchema
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

@api.post("/create-company", auth=CustomAuth())
def create_comp(request, payload:CreateSchema):
    user = request.auth
    if not user:
        raise HttpError(404, "User not found")
    Company.objects.create(
        name=payload.name,
        handled_by=user,
        gstin=payload.gstin,
        sector=payload.sector,
        pan=payload.pan,
        address=payload.address
            )
    return {"message": "Company successfully enrolled"}


@api.post("/upload", response=UploadResp, auth=CustomAuth())
def upload_file(request, payload:UploadSchema):
    user = request.auth
    if not user:
        raise HttpError(404, "User not found")
    company=get_object_or_404(Company, name=payload.name, handled_by=user)
    file_id = str(uuid.uuid4())
    key = f"docs/{company.name}/{file_id}-{payload.file_name}"
    presigned_url=generate_url(key, 'put_object')
    return {"presigned_url": presigned_url, "file_key": key}

@api.post("/history", auth=CustomAuth(), response=List[HistorySchema])
def histo(request, payload:HistoryInpSchema):
    user=request.auth
    if not user:
        raise HttpError(404, "User not found")
    company=get_object_or_404(Company, handled_by=user, name=payload.name)
    history=History.objects.filter(company=company).order_by("-timestamp")[:50]
    return [{"timestamp": h.timestamp, "cam_content": h.cam_content, "file_key": h.file_key, "email":h.company.email, "file_url": generate_url(h.file_key, 'get_object')} for h in history] 
        
#TODO: Push job_id, status, gstin, companyName, sector variables,next_topic=research_done to topic=qualitative_notes in pubsub
@api.post("/research", auth=CustomAuth())
def rese(request, payload:ResearchSchema):
    user = request.auth
    if not user:
        raise HttpError(404, "User not found")
    company = get_object_or_404(Company, handled_by=user, name=payload.name)
    history = get_object_or_404(History, job_id=job_id, company=company)
    history.status = 'processing'
    history.save()
    message = {"job_id": payload.job_id, }  #message fill karo-> kal tak
    return {"status": "processing", "job_id": job_id}

    

#TODO: Push file key (from frontend), job_id, status, next_topic=extracted-done, bucket name, file_name(from frontend), file_type(from frontend) to topic=extraction-topic in pubsub
@api.post("/extract", auth=CustomAuth())
def extrac(request, payload:ExtractSchema):
    user=request.auth
    if not user:
        raise HttpError(404, "User not found")
    company=get_object_or_404(Company, name=payload.name, handled_by=user)
    job_id=str(uuid.uuid4())
    History.objects.create(company=company, file_key=payload.file_key, job_id=job_id, status="queued")
    #Push karna baaki hai bhai
    return {"job_id": job_id, "status": "queued"}
    
#TODO: Subscribe to aggregator topic, write to DB



