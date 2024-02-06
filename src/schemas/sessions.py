from pydantic import BaseModel

from datetime import datetime


class SessionSchema(BaseModel):
    id: int
    token: str
    expires_in: datetime
    user_id: int