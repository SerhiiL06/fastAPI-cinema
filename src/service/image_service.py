from fastapi import UploadFile


class ImageService:

    def save(self, image: UploadFile, genre: str = None):

        genre = genre if genre else "other"

        path_to_file = f"media/{genre}/{image.filename}"

        with open(path_to_file, "wb+") as file:
            image_file: bytes = image.file.read()
            file.write(image_file)

        return path_to_file
