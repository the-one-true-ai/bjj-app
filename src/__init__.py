from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from src.auth.routes import auth_router
from src.users.routes import user_router
from src.feedback.routes import feedback_router
from .errors import register_all_errors
from .middleware import register_middleware
from src.videos.routes import video_router

version = "v1"

description = """
A REST API for the BJJ app
    """

version_prefix =f"/api/{version}"


app = FastAPI(
    title="BJJ app",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Achal or Dan",
        "url": "https://aidvp.com/",
        "email": "bluebeltlegends@aidvp.com",
    },
    terms_of_service="httpS://example.com/tos",
    openapi_url=f"{version_prefix}/openapi.json"
)


register_middleware(app)
register_all_errors(app)



app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])
app.include_router(user_router, prefix=f"{version_prefix}/users", tags=["users"])
app.include_router(feedback_router, prefix=f"{version_prefix}/sessions", tags=["feedback sessions"])
app.include_router(video_router, prefix=f"{version_prefix}/videos", tags=["videos"])
