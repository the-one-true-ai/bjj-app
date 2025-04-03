from src.db.models import FeedbackSession, Messages, Coaches
from uuid import uuid4
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from src.auth.dependencies import (
    get_current_user,
)  # Assuming this function exists for fetching the current user
from src.users.service import CoachService, UserService
from uuid import UUID
from src.feedback.schemas import Input_forStudent_FeedbackSessionCreateSchema
from src.feedback.validators import FeedbackStatus
from sqlmodel import select

coach_service = CoachService()
user_service = UserService()


class FeedbackSessionService:
    async def _get_feedback_session(self, feedback_session_id, session: AsyncSession):
        statement = select(FeedbackSession).where(FeedbackSession.feedback_session_id == feedback_session_id)
        result = await session.exec(statement)
        messages = result.first()

        if result:
            return messages
        else:
            return None #TODO: Better error/null handling
        
    async def _get_past_messages(self, feedback_session_id: UUID, session: AsyncSession): #TODO: Add pagination for speed
        """Retrieve past messages from the database."""
        statement = select(Messages).where(Messages.feedback_session_id == feedback_session_id).order_by(Messages.created_at)
        result = await session.exec(statement)
        return result.all()


    async def _does_user_have_access(self, user_id: UUID, feedback_session_id: UUID, session: AsyncSession):
        feedback_session = await self._get_feedback_session(feedback_session_id=feedback_session_id, session=session)
        
        user_coach_id = await user_service._get_coachID_from_userID(user_id=user_id, session=session)
        if user_coach_id == feedback_session.coach_id:
            return True
        else:
            user_student_id = await user_service._get_studentID_from_userID(user_id=user_id, session=session)
            if user_student_id == feedback_session.student_id:
                return True
            else:
                return False
            
    async def send_message(self, sender_user_id, feedback_session_id, message: str, session: AsyncSession):
        new_message = Messages(
            feedback_session_id=feedback_session_id,
            sender_user_id=sender_user_id,
            message_content=message,
            message_type="Text"
        )
        session.add(new_message)
        await session.commit()
                
    async def get_all_feedback_sessions(self, user_id: UUID, session: AsyncSession):
        user_profile = await user_service.get_full_user_profile(
            user_id=user_id, session=session
        )
        feedback_sessions = {}

        if user_profile["coach_profile"]:
            coach_id = await user_service._get_coachID_from_userID(user_id, session)
            statement = select(FeedbackSession).where(
                FeedbackSession.coach_id == coach_id
            )
            result = await session.exec(statement)
            feedback_sessions["as_coach"] = result.all()

        if user_profile["student_profile"]:
            student_id = await user_service._get_studentID_from_userID(user_id, session)
            statement = select(FeedbackSession).where(
                FeedbackSession.student_id == student_id
            )
            result = await session.exec(statement)
            feedback_sessions["as_student"] = result.all()

        # If student_profile, search fact_feedbacksessions with the student_id
        # feedback_sessions['as_student'] = result

        return feedback_sessions

    async def create_feedback_session(
        self,
        student_id: UUID,
        new_session_data: Input_forStudent_FeedbackSessionCreateSchema,
        session: AsyncSession,
    ):
        try:
            # Fetch the coach and associated user
            coach, user = await coach_service.get_coach_by_username(
                new_session_data.coach_username, session
            )
            if not coach:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Coach not found"
                )  # TODO: Improve warnings

            # Now you can safely access coach_id
            feedback_session = FeedbackSession(
                student_id=student_id,
                coach_id=coach.coach_id,  # This should now work!
                title=new_session_data.title,
                status=FeedbackStatus.AWAITING_FEEDBACK,  # TODO: Add a more sensible status
            )

            session.add(feedback_session)
            await session.commit()  # Commit to assign feedback_session_id
            await session.refresh(
                feedback_session
            )  # Ensure feedback_session_id is available

            # Step 4: Create the first message in fact_messages (either welcome or session start message)
            message_content = (
                new_session_data.message if new_session_data.message else None
            )
            initial_message = Messages(
                feedback_session_id=feedback_session.feedback_session_id,
                sender_user_id=await user_service._get_userID_from_studentID(student_id=student_id, session=session),
                message_type="TEXT",  # Assuming TEXT for now #TODO: Have a smarter way of determining type of message.
                message_content=message_content,
            )
            session.add(initial_message)
            await session.commit() 

            return feedback_session  # Return the created feedback session

        except SQLAlchemyError as e:
            print(f"Database error creating feedback session: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )
