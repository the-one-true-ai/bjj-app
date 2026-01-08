import os
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.auth.dependencies import get_current_user
from src.r2.client import get_r2_client  # the boto3 client helper

# If you want DB checks:
# from sqlalchemy.ext.asyncio import AsyncSession
# from src.db.main import get_session

video_router = APIRouter()

class PresignUploadIn(BaseModel):
    recipient_id: str
    filename: str
    content_type: str  # "video/mp4"

@video_router.post("/presign-upload")
async def presign_upload(
    payload: PresignUploadIn,
    user=Depends(get_current_user),
):
    # sender is the logged-in user
    sender_id = str(user.user_id)

    # Basic safety: restrict to mp4 if you want
    if payload.content_type != "video/mp4":
        raise HTTPException(status_code=400, detail="Only video/mp4 allowed")

    # Use a predictable private prefix
    object_key = (
        f"private/{sender_id}/{payload.recipient_id}/"
        f"{uuid.uuid4()}-{payload.filename}"
    )

    s3 = get_r2_client()
    url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": os.environ["R2_BUCKET_NAME"],
            "Key": object_key,
            "ContentType": payload.content_type,  # must match the browser upload header
        },
        ExpiresIn=60 * 5,  # 5 minutes
    )

    # You can also return an expires_at for your DB record (30 days retention idea)
    expires_at = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()

    return {"upload_url": url, "object_key": object_key, "expires_at": expires_at}


class PresignDownloadIn(BaseModel):
    object_key: str

@video_router.post("/presign-download")
async def presign_download(
    payload: PresignDownloadIn,
    user=Depends(get_current_user),
):
    requester_id = str(user.user_id)

    # TODO (important): check DB that requester_id is sender OR recipient for this object_key
    # and that it is not expired.
    #
    # Example logic:
    # record = await video_service.get_by_key(payload.object_key, session)
    # if record is None or record.expires_at < now: raise 410/404
    # if requester_id not in (record.sender_id, record.recipient_id): raise 403

    s3 = get_r2_client()
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": os.environ["R2_BUCKET_NAME"],
            "Key": payload.object_key,
        },
        ExpiresIn=60 * 5,
    )

    return {"download_url": url}
