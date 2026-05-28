from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.exceptions import CustomException
from src.model.continuous_learning import ContinuousLearningClass
from src.model.cycle import CycleClass
from src.model.enum import CycleStatus, MocStatus, ProcessStatus
from src.model.licensure import LicensureClass
from src.model.moc import MocClass
from src.model.payment import PaymentClass


def _all_moc_items_complete(moc: MocClass) -> bool:
    p: PaymentClass = moc.payment
    l: LicensureClass = moc.licensure
    cl: ContinuousLearningClass = moc.continuous_learning

    if not p or not l or not cl:
        return False

    return all([
        p.portal_payment_status,
        p.examination_payment_status,
        p.certificate_payment_status,
        l.upload_license,
        l.upload_moc,
        l.upload_marksheet,
        cl.upload_proof,
        cl.certification_proof,
    ])


class MocStatusService:

    @staticmethod
    def recompute_moc_status(moc_id: UUID, db: Session) -> MocStatus:
        moc: MocClass = db.execute(
            select(MocClass).where(MocClass.moc_id == moc_id)
        ).scalars().first()
        if not moc:
            raise CustomException.NotFoundError("MOC")

        cycle: CycleClass = moc.cycle
        if not cycle:
            raise CustomException.NotFoundError("Cycle for MOC")

        today = date.today()

        if not _all_moc_items_complete(moc):
            new_status = MocStatus.INCOMPLETE
        else:
            # Completion date = today (the day the last item was toggled)
            deadline = cycle.end_date               # 3-year mark
            grace = cycle.end_date + timedelta(days=365)  # 4-year mark

            if today <= deadline:
                new_status = MocStatus.PUNCTUAL
            elif today <= grace:
                new_status = MocStatus.DELAYED
            else:
                new_status = MocStatus.DANGEROUSLY_DELAYED

        moc.moc_status = new_status
        db.commit()

        # Propagate to cycle
        MocStatusService._recompute_cycle_status(cycle, db)
        return new_status

    @staticmethod
    def _recompute_cycle_status(cycle: CycleClass, db: Session) -> None:
        """
        Cycle is ACTIVE until MOC is resolved.
        Once MOC resolves: copy MOC status onto cycle.
        If DANGEROUSLY_DELAYED → cycle becomes DANGEROUSLY_DELAYED (blocks reassessment).
        """
        moc: MocClass = cycle.mocs[0] if cycle.mocs else None
        if not moc or moc.moc_status == MocStatus.INCOMPLETE:
            cycle.cycle_status = CycleStatus.ACTIVE
        elif moc.moc_status == MocStatus.PUNCTUAL:
            cycle.cycle_status = CycleStatus.PUNCTUAL
        elif moc.moc_status == MocStatus.DELAYED:
            cycle.cycle_status = CycleStatus.DELAYED
        elif moc.moc_status == MocStatus.DANGEROUSLY_DELAYED:
            cycle.cycle_status = CycleStatus.DANGEROUSLY_DELAYED

        db.commit()
