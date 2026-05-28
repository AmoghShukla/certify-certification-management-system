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
            # Validate MOC is not dangerously delayed before allowing reassessment
            cycle_number_to_check = cycle.cycle_number - 2
            moc = cycle.mocs[cycle_number_to_check] if cycle.mocs else None
            if moc and moc.moc_status == MocStatus.DANGEROUSLY_DELAYED:
                cert.certification_status = CertificationStatus.WITHDRAWN
                db.commit()
                return {
                    "message": (
                        "Certificate withdrawn. After 3 cycles, MOC was dangerously delayed "
                        "— reassessment not permitted."
                    ),
                    "certification_id": str(cert.certification_id),
                    "certification_status": CertificationStatus.WITHDRAWN.value,
                }
            return {
                "message": (
                    f"Cycle {cycle.cycle_number} complete. You must schedule a REASSESSMENT "
                    "examination to renew your certificate. Please book a REASSESSMENT slot."
                ),
                "action_required": "REASSESSMENT",
                "certification_id": str(cert.certification_id),
                "current_cycle_number": cycle.cycle_number,
            }

        cert.certification_status = CertificationStatus.INACTIVE
        today = date.today()
        valid_until = today + timedelta(days=THREE_YEARS_DAYS)
        new_renewal_count = cert.renewal_count + 1

        new_cert = CertificationClass(
            user_id=user_id,
            issued_date=today,
            valid_until=valid_until,
            renewal_count=new_renewal_count,
            certification_status=CertificationStatus.ACTIVE,
        )
        db.add(new_cert)
        db.flush()

        new_cycle_number = cycle.cycle_number + 1
        new_cycle = CycleClass(
            user_id=user_id,
            certification_id=new_cert.certification_id,
            cycle_number=new_cycle_number,
            start_date=today,
            end_date=valid_until,
        )
        db.add(new_cycle)
        db.flush()

        _create_moc_with_children(new_cycle.cycle_id, db)
        db.commit()

        return {
            "message": "Certificate renewed successfully.",
            "new_certification_id": str(new_cert.certification_id),
            "new_cycle_id": str(new_cycle.cycle_id),
            "new_cycle_number": new_cycle_number,
            "issued_date": str(today),
            "valid_until": str(valid_until),
        }
