from pydantic import BaseModel, HttpUrl


class UrlUploadModel(BaseModel):
    url: HttpUrl
