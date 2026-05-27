from .auth import AuthRepository
from .examination_slot import ExaminationSlotRepository
from .moc import MocRepository
from .promotions import PromotionsRepository
from .user import UserRepository
from .user_role import UserRoleRepository

__all__ = ['AuthRepository', 'ExaminationSlotRepository', 'MocRepository', 'PromotionsRepository', 'UserRepository', 'UserRoleRepository']