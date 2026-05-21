from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from app.schemas.url import URLShortenRequest, URLShortenResponse
from app.storage.memory import storage
from app.services.generator import CodeGenerator

router = APIRouter()

@router.post(
    "/shorten",
    response_model=URLShortenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Shorten a long URL",
    description="Accepts a long URL, generates a unique short code, stores it in memory, and returns the shortened link."
)
async def shorten_url(payload: URLShortenRequest, request: Request):
    original_url = str(payload.original_url)
    
    # Generate a unique code and handle collisions
    attempts = 0
    max_attempts = 10
    short_code = None
    
    while attempts < max_attempts:
        code = CodeGenerator.generate()
        if not storage.code_exists(code):
            short_code = code
            break
        attempts += 1
        
    if not short_code:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate a unique short code. Please try again."
        )
        
    # Save the mapping
    storage.save_url(short_code, original_url)
    
    # Construct the full short URL using the incoming request's base URL
    base_url = str(request.base_url)  # e.g., "http://127.0.0.1:8000/"
    if not base_url.endswith("/"):
        base_url += "/"
    short_url = f"{base_url}{short_code}"
    
    return URLShortenResponse(
        original_url=original_url,
        short_code=short_code,
        short_url=short_url
    )

@router.get(
    "/{short_code}",
    summary="Redirect short URL to original",
    description="Looks up the original URL for a short code and redirects the client with a HTTP 307 (Temporary Redirect)."
)
async def redirect_to_url(short_code: str):
    original_url = storage.get_url(short_code)
    
    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested short code was not found."
        )
        
    # DESIGN CHOICE: We use HTTP 307 Temporary Redirect instead of 301 Permanent Redirect.
    # 301 is cached by the browser, meaning future clicks would bypass our server entirely.
    # Since we plan to build an analytics dashboard in later milestones, 307 ensures 
    # every single redirect request goes through our server, enabling accurate metrics.
    return RedirectResponse(url=original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
