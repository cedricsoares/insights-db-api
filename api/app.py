import sqlite3
from datetime import datetime
from flask_openapi3 import Info, OpenAPI, Tag
from pydantic import BaseModel, Field
from typing import Optional

from api.constants import DB_PATH

API_DB_PATH = DB_PATH

info = Info(
    title="Insights DB API",
    version="1.0.0",
    description="API to manage pages in a SQLite database",
)

app = OpenAPI(__name__, info=info)

# Tags for categorizing endpoints
page_tag = Tag(name="page", description="Endpoints related to pages")


# Response models
class NotFoundResponse(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field("Resource not found!", description="Exception Information")


class InternalError(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field("Internal Error!", description="Exception Information")


# Request and response models for the page
class PagePath(BaseModel):
    id: int = Field(..., description="Page ID", example=1)


class PageBody(BaseModel):
    id: int = Field(..., description="Page ID", example=1)
    name: str = Field(..., description="Name of the page", example="fake_name")
    created_at: Optional[datetime] = Field(
        None, description="Page creation date", example="2023-01-01T00:00:00"
    )


class PageResponse(BaseModel):
    code: int = Field(0, description="Status Code")
    message: str = Field("ok", description="Exception Information")
    data: Optional[PageBody] = None


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
    conn = sqlite3.connect(API_DB_PATH)
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
        conn.close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
