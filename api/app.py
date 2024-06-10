from datetime import datetime
from flask_openapi3 import Info, OpenAPI, Tag
from pydantic import BaseModel, Field
from typing import Optional


info = Info(title="insigts db api", version="1.0.0")

app = OpenAPI(__name__)

page_tag = Tag(name="page", descripion="a page")


class PagePath(BaseModel):
    id: int = Field(..., description="Page id")


class PageBody(BaseModel):
    id: int = Field(..., description="Page id")
    name: str = Field(..., description="Name of page")
    created_at: Optional[datetime] = Field(..., description="Page creation date")


class PageResponse(BaseModel):
    code: int = Field(0, description="Status Code")
    message: str = Field("ok", description="Exception Information")
    data: Optional[PageBody]


""" @app.route("/")
def hello_world():
    return "Hello, World!" """


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
