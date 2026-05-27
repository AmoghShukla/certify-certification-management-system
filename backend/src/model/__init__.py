"""
Model package — import order matters for SQLAlchemy mapper configuration.

Rules
-----
* Base models (no FK deps) first: UserClass
* Dependent models follow their parent; never import a child before its parent.
* __all__ is provided so `from src.model import *` is explicit and safe.
* `all_models` is kept for Alembic env.py which iterates it to ensure every
  mapper is registered before `Base.metadata` is inspected.

FIXES
-----
* __all__ was commented out entirely — re-enabled and corrected the two
  misspelled names (`ExminationSlotClass` → `ExaminationSlotClass`,
  `UserExminationSlotClass` → `UserExaminationSlotClass`).
* Import order now follows FK dependency tree so circular-import risk is
  minimised (UserClass → UserRoleClass/CycleClass/CertificationClass →
  MocClass → PaymentClass/LicensureClass/ContinuousLearningClass,
  ExaminationSlotClass → UserExaminationSlotClass).
"""

from .user import UserClass
from .user_role import UserRoleClass
from .cycle import CycleClass
from .certification import CertificationClass
from .moc import MocClass
from .payment import PaymentClass
from .licensure import LicensureClass
from .continuous_learning import ContinuousLearningClass
from .slot import ExaminationSlotClass
from .user_examination_slot import UserExaminationSlotClass
from .examination import ExaminationClass

__all__ = [
    "UserClass",
    "UserRoleClass",
    "CycleClass",
    "CertificationClass",
    "MocClass",
    "PaymentClass",
    "LicensureClass",
    "ContinuousLearningClass",
    "ExaminationSlotClass",
    "UserExaminationSlotClass",
    "ExaminationClass",
]

all_models = [
    UserClass,
    UserRoleClass,
    CycleClass,
    CertificationClass,
    MocClass,
    PaymentClass,
    LicensureClass,
    ContinuousLearningClass,
    ExaminationSlotClass,
    UserExaminationSlotClass,
    ExaminationClass,
]