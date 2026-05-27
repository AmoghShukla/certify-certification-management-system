from pydantic import BaseModel
from uuid import UUID

from backend.src.model.enum import MocStatus

class MocRequest(BaseModel):
    cycle_id : UUID

class MocResponse(BaseModel):
    moc_id : UUID
    cycle_id : UUID
    moc_status : MocStatus