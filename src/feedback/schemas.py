from pydantic import BaseModel, HttpUrl

class Input_forStudent_FeedbackSessionCreateSchema(BaseModel):
    title: str
    video: HttpUrl
    message: str
    coach_username: str

# TODO: Create a ResponseSchema    