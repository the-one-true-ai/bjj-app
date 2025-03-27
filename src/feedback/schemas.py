from pydantic import BaseModel, HttpUrl, Field

class Input_forStudent_FeedbackSessionCreateSchema(BaseModel):
    title: str = Field(min_length=5, max_length=30, description="The title of the feedback session.")
    video: HttpUrl = Field(min_length=5, max_length=200, description="The URL of the video file used to initiate feedback session.")
    message: str = Field(default="Hi! Please checkout my video below.", min_length=20, max_length=300, description="The initial message sent to initiate feedback session.")
    coach_username: str =Field(description="The username of the coach selected.")

# TODO: Create a ResponseSchema    