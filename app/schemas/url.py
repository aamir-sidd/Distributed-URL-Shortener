from pydantic import BaseModel, HttpUrl, Field

class URLShortenRequest(BaseModel):
    """Pydantic schema to validate the incoming URL shortening request.
    Using Pydantic's built-in HttpUrl ensures the input is a valid web address"""
    original_url: HttpUrl = Field(
        ...,
        description="The original target URL to shorten.",
        examples=["https://github.com/fastapi/fastapi"]
    )

class URLShortenResponse(BaseModel):
    """Pydantic schema representing the successfully shortened URL response"""
    original_url: str = Field(..., description="The original long target URL.")
    short_code: str = Field(..., description="The generated unique short identifier.")
    short_url: str = Field(..., description="The fully qualified shortened redirect URL.")
