import sqlite3
from datetime import datetime
from flask_openapi3 import Info, OpenAPI, Tag
from pydantic import BaseModel, Field
from typing import Optional

from api.constants import DB_PATH

# Instanciation de l'application OpenAPI
info = Info(
    title="Insights DB API",
    version="1.0.0",
    description="API to manage pages and videos in a SQLite database",
)
app = OpenAPI(__name__, info=info)


page_tag = Tag(name="page", description="Endpoints related to pages")
video_tag = Tag(name="video", description="Endpoints related to videos")


class NotFoundResponse(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field("Resource not found!", description="Exception Information")


class InternalError(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field("Internal Error!", description="Exception Information")


class PagePath(BaseModel):
    id: int = Field(..., description="Page ID")


class PageBody(BaseModel):
    id: int = Field(..., description="page id")
    name: str = Field(..., description="Name of the page")
    created_at: Optional[datetime] = Field(None, description="Page creation date")


class PageResponse(BaseModel):
    code: int = Field(0, description="Status Code")
    message: str = Field("ok", description="Exception Information")
    data: Optional[PageBody] = None


class PageAddedResponse(BaseModel):
    code: int = Field(0, description="Status Code")
    message: str = Field(
        "Page added successfully!", description="Exception Information"
    )
    data: Optional[dict] = None


class VideoPath(BaseModel):
    id: int = Field(..., description="Video ID")


class VideoBody(BaseModel):
    id: int = Field(..., description="ID of the video")
    page_id: int = Field(..., description="ID of the page to which the video belongs")
    title: str = Field(..., description="Title of the video")
    created_at: Optional[datetime] = Field(None, description="Video creation date")


class VideoResponse(BaseModel):
    code: int = Field(..., description="Status Code")
    message: str = Field("ok", description="Exception Information")
    data: Optional[VideoBody] = None


class VideoAddedResponse(BaseModel):
    code: int = Field(0, description="Status Code")
    message: str = Field(
        "Video added successfully!", description="Exception Information"
    )
    data: Optional[dict] = None


# Routes pour les pages
@app.post(
    "/page",
    tags=[page_tag],
    summary="Add a new page",
    description="Add a new page to the database",
    operation_id="add_page",
    responses={200: PageAddedResponse, 500: InternalError},
)
def add_page(body: PageBody):
    """
    Endpoint to add a new page.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO pages (id, name) VALUES (?, ?)",
            (
                body.id,
                body.name,
            ),
        )
        conn.commit()

        new_page_id = cur.lastrowid

        return {
            "code": 0,
            "message": "Page added successfully!",
            "data": {"id": new_page_id, "name": body.name},
        }

    except Exception:
        return InternalError().model_dump(), 500

    finally:
        cur.close()
        conn.close()


@app.get(
    "/page/<int:id>",
    tags=[page_tag],
    summary="Retrieve page description",
    description="Retrieve the details of a page using its ID",
    operation_id="get_page_by_id",
    responses={
        200: PageResponse,
        404: NotFoundResponse,
        500: InternalError,
    },
)
def get_page(path: PagePath):
    """
    Endpoint to retrieve page details.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        page = cur.execute(
            "SELECT id, name, created_at FROM pages WHERE id = ?", (path.id,)
        ).fetchone()

        if not page:
            return NotFoundResponse().model_dump(), 404

        return {
            "code": 0,
            "message": "ok",
            "data": {"id": path.id, "name": page[1], "created_at": page[2]},
        }

    except Exception:
        return InternalError().model_dump(), 500

    finally:
        cur.close()
        conn.close()


@app.delete(
    "/page/<int:id>",
    tags=[page_tag],
    summary="Delete a page",
    description="Delete a page from the database using its ID",
    operation_id="delete_page",
    responses={200: PageResponse, 404: NotFoundResponse, 500: InternalError},
)
def delete_page(path: PagePath):
    """
    Endpoint to delete a page.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM pages WHERE id = ?", (path.id,))
        conn.commit()

        if cur.rowcount == 0:
            return NotFoundResponse().model_dump(), 404

        return {
            "code": 0,
            "message": "Page deleted successfully!",
            "data": {"id": path.id},
        }

    except Exception:
        return InternalError().model_dump(), 500

    finally:
        cur.close()
        conn.close()


@app.post(
    "/video",
    tags=[video_tag],
    summary="Add a new video",
    description="Add a new video to the database",
    operation_id="add_video",
    responses={200: VideoAddedResponse, 500: InternalError},
)
def add_video(body: VideoBody):
    """
    Endpoint to add a new video.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO videos (id, page_id, title) VALUES (?, ?, ?)",
            (body.id, body.page_id, body.title),
        )
        conn.commit()

        new_video_id = cur.lastrowid

        return {
            "code": 0,
            "message": "Video added successfully!",
            "data": {"id": new_video_id, "page_id": body.page_id, "title": body.title},
        }

    except Exception:
        return InternalError().model_dump(), 500

    finally:
        cur.close()
        conn.close()


@app.get(
    "/vdeo/<int:id>",
    tags=[video_tag],
    summary="Retrieve page description",
    description="Retrieve the details of a page using its ID",
    operation_id="get_video_by_id",
    responses={
        200: PageResponse,
        404: NotFoundResponse,
        500: InternalError,
    },
)
def get_video(path: VideoPath):
    """
    Endpoint to retrieve page details.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        video = cur.execute(
            "SELECT id, page_id, title, created_at FROM videos WHERE id = ?", (path.id,)
        ).fetchone()

        if not video:
            return NotFoundResponse().model_dump(), 404

        return {
            "code": 0,
            "message": "ok",
            "data": {
                "id": path.id,
                "page_id": video[1],
                "title": video[2],
                "created_at": video[3],
            },
        }

    except Exception:
        return InternalError().model_dump(), 500

    finally:
        cur.close()
        conn.close()


@app.delete(
    "/video/<int:id>",
    tags=[video_tag],
    summary="Delete a video",
    description="Delete a video from the database using its ID",
    operation_id="delete_video",
    responses={200: VideoResponse, 404: NotFoundResponse, 500: InternalError},
)
def delete_video(path: VideoPath):
    """
    Endpoint to delete a video.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM videos WHERE id = ?", (path.id,))
        conn.commit()

        if cur.rowcount == 0:
            return NotFoundResponse().model_dump(), 404

        return {
            "code": 0,
            "message": "Video deleted successfully!",
            "data": {"id": path.id},
        }

    except Exception:
        return InternalError().model_dump(), 500

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
