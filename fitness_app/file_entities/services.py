import os
import uuid
from tempfile import NamedTemporaryFile

import boto3
from botocore.exceptions import ClientError
from fastapi import BackgroundTasks, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from fitness_app.core.exceptions import (
    EntityNotFoundException,
    ForbiddenException,
    InternalServerError,
)
from fitness_app.file_entities.models import FileEntity
from fitness_app.file_entities.repositories import FileEntityRepository


class FileEntityService:
    def __init__(
        self,
        region: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        bucket_name: str,
        aws_endpoint: str,
        aws_access_domain_name: str,
        file_entity_repository: FileEntityRepository,
    ):
        self._region = region
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._bucket_name = bucket_name
        self._aws_endpoint = aws_endpoint
        self._aws_access_domain_name = aws_access_domain_name
        self._file_entity_repository = file_entity_repository
        self._s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region,
            endpoint_url=aws_endpoint,
        )

    async def add_to_s3(self, file: UploadFile):
        cur_uuid = str(uuid.uuid4())
        _, file_extension = os.path.splitext(file.filename)
        if file_extension:
            cur_uuid += file_extension

        try:
            self._s3_client.upload_fileobj(file.file, self._bucket_name, cur_uuid)
        except ClientError as e:
            raise InternalServerError(str(e))

        return cur_uuid

    async def create(self, session: AsyncSession, file: UploadFile, exercise_id: int):
        new_filename = await self.add_to_s3(file)
        file_entity = FileEntity(filename=new_filename, exercise_id=exercise_id)
        return await self._file_entity_repository.save(session, file_entity)

    async def get_by_filename(self, session: AsyncSession, filename: str):
        file_entity = await self._file_entity_repository.get_by_filename(
            session, filename
        )
        if not file_entity:
            raise EntityNotFoundException(
                "FileEntity with given filename was not found"
            )

        return self._aws_access_domain_name + filename

    async def delete_by_id(self, session: AsyncSession, id: int):
        file_entity = await self._file_entity_repository.get_by_id(session, id)
        if file_entity is None:
            raise EntityNotFoundException("FileEntity with given id was not found")
        try:
            self._s3_client.delete_object(
                Bucket=self._bucket_name, Key=file_entity.filename
            )
        except ClientError as e:
            raise InternalServerError(str(e))

        return await self._file_entity_repository.delete(session, file_entity)