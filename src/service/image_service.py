from fastapi import UploadFile, HTTPException


class ImageService:

    def save(self, image: UploadFile, genre: str = None):

        genre = genre[0] if genre else "other"

        path_to_file = f"media/{genre}/{image.filename}"
        try:
            with open(path_to_file, "wb+") as file:
                image_file: bytes = image.file.read()
                file.write(image_file)

            return path_to_file

        except FileNotFoundError as e:
            raise HTTPException(400, "error image saved")
