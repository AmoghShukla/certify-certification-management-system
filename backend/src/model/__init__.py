from .user import UserClass
from .user_role import UserRoleClass
from .certification import CertificationClass
from .continuous_learning import ContinuousLearningClass
from .cycle import CycleClass
from .examination import ExaminationClass
from .licensure import LicensureClass
from .user_examination_slot import UserExaminationSlotClass
from .moc import MocClass
from .payment import PaymentClass
from .slot import ExaminationSlotClass


# __all__=[
#     'UserClass',
#     'UserRoleClass',
#     'CertificationClass',
#     'ContinuousLearningClass',
#     'CycleClass',
#     'ExaminationClass',
#     'LicensureClass',
#     'MocClass',
#     'PaymentClass',
#     'ExminationSlotClass',
#     'UserExminationSlotClass'
# ]

all_models = [
    UserClass,
    UserRoleClass,
    CertificationClass,
    ContinuousLearningClass,
    CycleClass,
    ExaminationClass,
    LicensureClass,
    MocClass,
    PaymentClass,
    ExaminationSlotClass,
    UserExaminationSlotClass
]