from pydantic import BaseModel
from backend.src.model.enum import ExaminationType
from datetime import date, datetime, time, timedelta, timezone
from pydantic import BaseModel, Field, field_validator, UUID4
from backend.src.model.enum import ExaminationType

IST = timezone(timedelta(hours=5, minutes=30))

class ExaminationCreate(BaseModel):
    examination_date: date
    examination_type: ExaminationType
    examination_slot_start_time: time = Field(description="Must include IST timezone")
    examination_slot_end_time: time = Field(description="Must include IST timezone")
    examination_slot_total_capacity: int

class ExaminationResponse(BaseModel):
    examination_slot_id : UUID4
    examination_date : date
    examination_type : ExaminationType
    examination_slot_start_time : time
    examination_slot_end_time : time
    examination_slot_total_capacity : int
    examination_slot_available_capacity : int