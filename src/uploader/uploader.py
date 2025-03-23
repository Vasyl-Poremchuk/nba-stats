import logging
import os
from pathlib import Path

import boto3

from common.constants import BaseConstants, LoggerConstants
from common.logger import init_logger

init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)


class Uploader:
    def __init__(self) -> None:
        self._client_name = "s3"

    @staticmethod
    def make_base_folder(base_folder: Path) -> None:
        """Create a base folder if it doesn't exist.

        :param base_folder: A folder to create.
        :return: None.
        """
        os.makedirs(base_folder, exist_ok=True)

    def _get_s3_client(self) -> boto3.client:
        """Initialize an S3 client.

        :return: S3 client.
        """
        s3_client = boto3.client(self._client_name)

        return s3_client

    @staticmethod
    def extract_file_key(filepath: Path) -> str:
        """Extract a file key as the combination of the inner folder
        and the filename.

        :param filepath: A filepath from which to extract the file key.
        :return: Key.
        """
        folder = filepath.parts[-3]
        inner_folder = filepath.parts[-2]
        filename = filepath.name

        file_key = f"{folder}/{inner_folder}/{filename}"

        return file_key

    def _upload_file_to_s3(self, filepath: Path, bucket: str) -> None:
        """Upload the specified file to an S3 bucket.

        :return: None.
        """
        s3_client = self._get_s3_client()
        file_key = self.extract_file_key(filepath=filepath)

        s3_client.upload_file(
            Filename=filepath,
            Bucket=bucket,
            Key=file_key,
        )

    @staticmethod
    def get_filepaths(base_folder: Path, extensions: tuple) -> list[Path]:
        """Get a list of filepaths to upload.

        :param base_folder: A base folder of the files.
        :param extensions: Extensions of the files.
        :return: Filepaths.
        """
        filepaths = [
            base_folder.joinpath(filename)
            for filename in os.listdir(base_folder)
            if filename.endswith(extensions)
        ]

        return filepaths

    def upload_files_to_s3(self, base_folder: Path, extensions: tuple) -> None:
        """Upload files to an S3 bucket.

        :param base_folder: A base folder of the files.
        :param extensions: Extensions of the files.
        :return: None.
        """
        filepaths = self.get_filepaths(
            base_folder=base_folder, extensions=extensions
        )

        for filepath in filepaths:
            self._upload_file_to_s3(
                filepath=filepath, bucket=BaseConstants.S3_BUCKET
            )

            logger.info(
                msg=f"`{filepath.name}` uploaded to "
                f"`{BaseConstants.S3_BUCKET}` S3 bucket."
            )
