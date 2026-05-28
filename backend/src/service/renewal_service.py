from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.exceptions import CustomException
from src.model.certification import CertificationClass
from src.model.continuous_learning import ContinuousLearningClass
from src.model.cycle import CycleClass
from src.model.enum import (
    CertificationStatus,
    CycleStatus,
    ExaminationType,
    MocStatus,
)
from src.model.licensure import LicensureClass
from src.model.moc import MocClass
from src.model.payment import PaymentClass
from src.model.user_examination_slot import UserExaminationSlotClass

THREE_YEARS_DAYS = 365 * 3


def _create_moc_with_children(cycle_id: UUID, db: Session) -> MocClass:
    from src.model.enum import MocStatus
    moc = MocClass(cycle_id=cycle_id, moc_status=MocStatus.INCOMPLETE)
    db.add(moc)
    db.flush()
    db.add(PaymentClass(moc_id=moc.moc_id))
    db.add(LicensureClass(moc_id=moc.moc_id))
    db.add(ContinuousLearningClass(moc_id=moc.moc_id))
    return moc


class RenewalService:

    @staticmethod
    def _get_cycle_by_number(
        user_id: UUID,
        cycle_number: int,
        db: Session
    ) -> CycleClass | None:
        return db.execute(
            select(CycleClass).where(
                CycleClass.user_id == user_id,
                CycleClass.cycle_number == cycle_number,
                CycleClass.is_deleted == False,
            )
        ).scalars().first()

    @staticmethod
    def renew_certificate(user_id: UUID, db: Session) -> dict:
        cert = db.execute(
            select(CertificationClass).where(
                CertificationClass.user_id == user_id,
                CertificationClass.certification_status == CertificationStatus.ACTIVE,
                CertificationClass.is_deleted == False
            )
        ).scalars().first()

        if not cert:
            raise CustomException.NotFoundError("Active Certification for user")

        cycle = db.execute(
            select(CycleClass).where(
                CycleClass.certification_id == cert.certification_id,
                CycleClass.is_deleted == False
            ).order_by(CycleClass.cycle_number.desc())
        ).scalars().first()

        if not cycle:
            raise CustomException.NotFoundError("Cycle for certification")

        if cycle.cycle_status == CycleStatus.DANGEROUSLY_DELAYED:
            cert.certification_status = CertificationStatus.WITHDRAWN
            db.commit()
            return {
                "message": "Certificate withdrawn. MOC was dangerously delayed : renewal denied.",
                "certification_id": str(cert.certification_id),
                "certification_status": CertificationStatus.WITHDRAWN.value,
            }

        if cycle.cycle_number % 3 == 0:

            reference_cycle_number = cycle.cycle_number - 2

            reference_cycle = RenewalService._get_cycle_by_number(
                user_id=user_id,
                cycle_number=reference_cycle_number,
                db=db,
            )

            reference_moc = (reference_cycle.mocs[0] if reference_cycle and reference_cycle.mocs else None)

            if (reference_moc and reference_moc.moc_status == MocStatus.DANGEROUSLY_DELAYED):
                cert.certification_status = CertificationStatus.WITHDRAWN
                db.commit()

                return {
                    "message": (
                        f"Certificate withdrawn. "
                        f"Reference cycle {reference_cycle_number} MOC "
                        f"was dangerously delayed."
                    ),
                    "certification_id": str(cert.certification_id),
                    "certification_status": CertificationStatus.WITHDRAWN.value,
                }

            return {
                "message": (
                    f"Cycle {cycle.cycle_number} complete. "
                    f"You must schedule a REASSESSMENT examination "
                    f"to renew your certificate."
                ),
                "action_required": "REASSESSMENT",
                "certification_id": str(cert.certification_id),
                "current_cycle_number": cycle.cycle_number,
                "reference_cycle_checked": reference_cycle_number,
            }