import os
from pathlib import Path

from fastapi import HTTPException, UploadFile


class ImageService:

    def save(self, image: UploadFile, genre: list[str] = None):

        genre = genre if genre else "other"

        path_to_file = f"media/{genre}/{image.filename}"
        try:
            with open(path_to_file, "wb+") as file:
                image_file: bytes = image.file.read()
                file.write(image_file)

            return path_to_file

        except FileNotFoundError as e:
            print(e)
            raise HTTPException(400, "error image saved")

    def delete(self, path: str):

        if Path(path).exists():
            os.remove(path)
        else:
            raise FileNotFoundError("file not found")
