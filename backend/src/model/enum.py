from enum import Enum

class UserTitle(Enum):
    Mr = "Mr"
    Ms = "Ms"
    Dr = "Dr"
    Mrs = "Mrs"

class UserRole(Enum):
    ADMIN = "ADMIN"
    SUPERADMIN = "SUPERADMIN"
    USER = "USER"
    CANDIDATE = "CANDIDATE"
    DIPLOMATE = "DIPLOMATE"

ROLE_HIERARCHY: dict[str, int] = {
    "USER": 1,
    "CANDIDATE": 2,
    "DIPLOMATE": 3,
    "ADMIN": 4,
    "SUPERADMIN": 5,
}

def highest_role(roles: list[str]) -> str:
    return max(roles, key=lambda r: ROLE_HIERARCHY.get(r, 0))
 

class UserExaminationStatus(Enum):
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"

class ExaminationType(Enum):
    ASSESMENT = "ASSESMENT"
    REASSESMENT = "REASSESMENT"

class MocStatus(Enum):
    INCOMPLETE = "INCOMPLETE"
    PUNCTUAL = "PUNCTUAL"
    DELAYED = "DELAYED"
    DANGEROUSLY_DELAYED = "DANGEROUSLY_DELAYED"

class CertificationStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    LOST = "LOST"

class ProcessStatus(Enum):
    INCOMPLETE = "INCOMPLETE"
    COMPLETED = "COMPLETED"

class PaymentStatus(Enum):
    COMPLETED = "COMEPLETED"
    PENDING = "PENDING"
    REFUNDED = "REFUNDED"