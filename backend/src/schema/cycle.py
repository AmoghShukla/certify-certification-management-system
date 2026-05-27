from datetime import date, datetime

from pydantic import BaseModel
from uuid import UUID

from backend.src.model.enum import MocStatus

class CycleRequest(BaseModel):
    user_id : UUID
    cycle_number : int
    start_date  : date
    end_date : date

class CycleResponse(BaseModel):
    cycle_id : UUID
    user_id : UUID
    cycle_number : int
    start_date  : date
    end_date : date
    updated_at : datetime