import sys
from typing import List

from fastapi import APIRouter, HTTPException, File, UploadFile, Response

from controllers.videos_controller import VideosController
from models.url_upload import UrlUploadModel
from services.downloaders.video_downloader import VideoDownloader

router = APIRouter(prefix="/videos")

videos_controller = VideosController()


@router.get("/")
def videos():
    return videos_controller.get_top_videos()


@router.get("/{video_id}")
def get_video(video_id: str):
    video = videos_controller.get_video(video_id)
    media_convert_job_id = video.get("media_convert_job_id")
    if not media_convert_job_id:
        raise HTTPException(404, "Video not found")
    job_status = video.get("status")
    if job_status == "ERROR":
        raise HTTPException(400, "Invalid Video Uploaded")
    elif job_status == "PROGRESSING" or job_status == "SUBMITTED":
        return {"status": job_status}
    updated_video = videos_controller.increment_views(video_id)
    return {
        "views": updated_video["views"],
        "created_at": updated_video["created_at"],
        "video_id": updated_video["id"],
        "video_title": updated_video.get("video_title"),
        "status": updated_video["status"],
    }


@router.post("/upload/files")
def upload_multiple_files(files: List[UploadFile] = File(...)):
    video_item = videos_controller.upload_multiple_videos_as_one(
        [file.file.read() for file in files]
    )
    return {"id": video_item["id"]}


@router.post("/upload")
def upload_video(file: UploadFile = File(...)):
    raise HTTPException(400, "Stahp! Video Uploading is Stopped Currently")
    video_item = videos_controller.upload_video(file.file.read())
    return {"id": video_item["id"]}


@router.post("/upload-from-url")
def upload_video_from_url(url_upload_model: UrlUploadModel):
    raise HTTPException(400, "Stahp! Video Uploading is Stopped Currently")
    file = VideoDownloader(url_upload_model.url).get_video_content()
    if not file:
        raise HTTPException(400, "Website not supported")
    file_size = sys.getsizeof(file)
    if file_size > 100000000:  # 100 MB
        raise HTTPException(400, "File too big")
    video_item = videos_controller.upload_video(file)
    return {"id": video_item["id"]}


@router.post("/{video_id}/report")
def report_video(video_id: str):
    videos_controller.report_video(video_id)
    return Response(status_code=204)


@router.get("/{video_id}/related")
def get_related_videos(video_id: str):
    return videos_controller.get_related_videos(video_id)
