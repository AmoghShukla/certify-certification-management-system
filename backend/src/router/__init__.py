from .auth import router as AuthRouter
from .user import router as UserRouter
from .promotions import router as PromotionsRouter
from .examination_slot import router as ExaminationRouter
from .moc import router as MocRouter

all = [AuthRouter, UserRouter, PromotionsRouter, ExaminationRouter, MocRouter]