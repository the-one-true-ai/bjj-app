from enum import Enum

class MessageType(str, Enum):
    TEXT = "Text"
    AUDIO = "Audio"
    VIDEO = "Video"

class FeedbackStatus(str, Enum):
    AWAITING_FEEDBACK = "Awaiting feedback"
    FEEDBACK_GIVEN = "Feedback given"