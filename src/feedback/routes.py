from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.db.main import get_session
from src.auth.dependencies import RoleChecker, get_current_user
from src.feedback.service import FeedbackSessionService
from src.feedback.schemas import Input_forStudent_FeedbackSessionCreateSchema
from fastapi import HTTPException
from fastapi import WebSocketDisconnect
from src.users.service import UserService
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

feedback_router = APIRouter()
feedback_service = FeedbackSessionService()
user_service = UserService()

active_connections = []  # Global list of active WebSocket connections

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/api/v1/sessions/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@feedback_router.get("/")
async def get():
    return HTMLResponse(html)

@feedback_router.websocket("/chat/{feedback_session_id}")
async def websocket_endpoint(websocket: WebSocket, feedback_session_id: UUID, session: AsyncSession = Depends(get_session)):
    # Call the method without passing 'feedback_session_id' explicitly
    past_messages = await feedback_service._get_past_messages(feedback_session_id=feedback_session_id, session=session)
    
    await websocket.accept()
    active_connections.append(websocket)

    for message in past_messages:
        await websocket.send_text(f"{message.sender_user_id} sent: {message.message_content}")

    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast the message to all connected clients
            for connection in active_connections:
                await connection.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)












@feedback_router.get("/get_my_feedback_sessions")
async def get_my_feedback_sessions(
    session: AsyncSession = Depends(get_session), user=Depends(get_current_user)
):
    get_my_feedback_sessions = await feedback_service.get_all_feedback_sessions(
        user_id=user.user_id, session=session
    )
    return get_my_feedback_sessions


@feedback_router.post(
    "/create_feedback_session", dependencies=[Depends(RoleChecker(["Student"]))]
)
async def create_feedback_session_route(
    new_session_data: Input_forStudent_FeedbackSessionCreateSchema,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    # Get the full profile for the logged-in user
    full_profile = await user_service.get_full_user_profile(
        user_id=user.user_id, session=session
    )

    # Extract the student_id from the full profile (accessing it as a key in the dictionary)
    student_id = full_profile["student_profile"].student_id

    # Now, pass the student_id to the service to create the feedback session
    feedback_session = await feedback_service.create_feedback_session(
        student_id=student_id, new_session_data=new_session_data, session=session
    )
    return feedback_session
