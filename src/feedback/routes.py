from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, get_current_user
from src.feedback.service import FeedbackSessionService
from src.feedback.schemas import Input_forStudent_FeedbackSessionCreateSchema
from fastapi import HTTPException
from src.users.service import UserService

feedback_router = APIRouter()
feedback_service = FeedbackSessionService()
user_service = UserService()

@feedback_router.post("/create_feedback_session")
# TODO: Limit this so that only students can access this
async def create_feedback_session_route(
    new_session_data: Input_forStudent_FeedbackSessionCreateSchema,
    session: AsyncSession = Depends(get_session),
    user = Depends(get_current_user)):

    # Get the full profile for the logged-in user
    full_profile = await user_service.get_full_user_profile(user_id=user.user_id, session=session)
    
    # Check if the student_profile exists (now accessed as a key in the dictionary)
    if not full_profile.get('student_profile'):
        raise HTTPException(
            status_code=400,
            detail="Student profile not found. Ensure the user is assigned as a student."
        )
     #TODO: Improve warnings
    
    # Extract the student_id from the full profile (accessing it as a key in the dictionary)
    student_id = full_profile['student_profile']['student_id']

    # Now, pass the student_id to the service to create the feedback session
    feedback_session = await feedback_service.create_feedback_session(
        student_id=student_id,
        new_session_data=new_session_data,
        session=session
    )

    return feedback_session

