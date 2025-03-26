from enum import Enum

class MessageType(str, Enum):
    TEXT = "Text"
    AUDIO = "Audio"
    VIDEO = "Video"

class FeedbackStatus(str, Enum): #TODO: Review this, doesnt really make that much sense
    AWAITING_FEEDBACK = "Awaiting feedback"
    FEEDBACK_GIVEN = "Feedback given"