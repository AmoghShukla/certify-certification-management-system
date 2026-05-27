from pathlib import Path
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError

from backend.src.utils.logger import get_logger
from backend.src.core.config import settings

logger = get_logger(__name__)

class S3Service:

    @staticmethod
    def upload_file(file, object_name=None):
        if object_name is None:
            file_name = Path(file.filename).suffix
            object_name = f"upload/user-certificates/{uuid4()}{file_name}"

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.REGION_NAME,
        )
        try:
            response = s3_client.upload_fileobj(
                file.file,
                settings.AWS_BUCKET_NAME,
                object_name,
                ExtraArgs={"ContentType": file.content_type or "application/octet-stream"},
            )
        except ClientError as e:
            logger.error(e)
            return False
        return object_name