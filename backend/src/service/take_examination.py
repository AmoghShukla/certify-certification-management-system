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
    PaymentStatus,
    UserExaminationStatus,
    UserRole,
)
from src.model.licensure import LicensureClass
from src.model.moc import MocClass
from src.model.payment import PaymentClass
from src.model.user_examination_slot import UserExaminationSlotClass
from src.model.user_role import UserRoleClass
from src.repository.user import UserRepository
from src.repository.user_role import UserRoleRepository

THREE_YEARS_DAYS = 365 * 3


def _replace_role(user_id: UUID, old_role: UserRole, new_role: UserRole, db: Session) -> None:
    """Soft-delete the old role row and insert the new one."""
    existing = db.execute(
        select(UserRoleClass).where(
            UserRoleClass.user_id == user_id,
            UserRoleClass.user_role == old_role,
            UserRoleClass.is_deleted == False,  # noqa: E712
        )
    ).scalars().first()
    if existing:
        existing.is_deleted = True

    new_row = UserRoleClass(user_id=user_id, user_role=new_role)
    db.add(new_row)


def _create_moc_with_children(cycle_id: UUID, db: Session) -> MocClass:
    """Create MOC + Payment + Licensure + ContinuousLearning for a cycle."""
    moc = MocClass(cycle_id=cycle_id, moc_status=MocStatus.INCOMPLETE)
    db.add(moc)
    db.flush()  # get moc.moc_id

    db.add(PaymentClass(moc_id=moc.moc_id))
    db.add(LicensureClass(moc_id=moc.moc_id))
    db.add(ContinuousLearningClass(moc_id=moc.moc_id))
    return moc


class TakeExaminationService:

    @staticmethod
    def take_examination(user_examination_slot_id: UUID, db: Session) -> dict:
        # ── 1. Fetch the booking ──────────────────────────────────────────────
        booking: UserExaminationSlotClass = db.execute(
            select(UserExaminationSlotClass).where(
                UserExaminationSlotClass.user_examination_slot_id == user_examination_slot_id,
                UserExaminationSlotClass.is_deleted == False,  # noqa: E712
            )
        ).scalars().first()

        if not booking:
            raise CustomException.NotFoundError("UserExaminationSlot")

        if booking.payment_status != PaymentStatus.COMPLETED:
            raise CustomException.BadRequestError(
                "Examination payment not completed. Please complete payment before taking the exam."
            )

        if booking.user_examination_status == UserExaminationStatus.COMPLETED:
            raise CustomException.BadRequestError("Examination has already been taken.")

        user_id = booking.user_id

        # ── 2. Mark exam as COMPLETED ────────────────────────────────────────
        booking.user_examination_status = UserExaminationStatus.COMPLETED

        # ── 3. Role transition ───────────────────────────────────────────────
        if booking.examination_type == ExaminationType.ASSESSMENT:
            # CANDIDATE → DIPLOMATE  (also ensure CANDIDATE exists)
            _replace_role(user_id, UserRole.CANDIDATE, UserRole.DIPLOMATE, db)
        else:
            # REASSESSMENT — user is already DIPLOMATE; just keep the role
            # (a new cert + cycle will be issued below)
            pass

        # ── 4. Issue Certificate ─────────────────────────────────────────────
        today = date.today()
        valid_until = today + timedelta(days=THREE_YEARS_DAYS)

        # Count existing certs to generate a readable cert number
        existing_certs_count = db.execute(
            select(CertificationClass).where(
                CertificationClass.user_id == user_id,
                CertificationClass.is_deleted == False,  # noqa: E712
            )
        ).scalars().all()
        renewal_count = len(existing_certs_count)

        cert = CertificationClass(
            user_id=user_id,
            user_examination_slot_id=user_examination_slot_id,
            issued_date=today,
            valid_until=valid_until,
            renewal_count=renewal_count,
            certification_status=CertificationStatus.ACTIVE,
        )
        db.add(cert)
        db.flush()  # get cert.certification_id

        # ── 5. Create Cycle ──────────────────────────────────────────────────
        cycle_number = renewal_count + 1  # 1st cert → cycle 1, 1st renewal → cycle 2 …
        cycle = CycleClass(
            user_id=user_id,
            certification_id=cert.certification_id,
            cycle_number=cycle_number,
            start_date=today,
            end_date=valid_until,
            cycle_status=CycleStatus.ACTIVE,
        )
        db.add(cycle)
        db.flush()

        # ── 6. Create MOC ────────────────────────────────────────────────────
        _create_moc_with_children(cycle.cycle_id, db)

        db.commit()

        return {
            "message": "Examination completed successfully.",
            "user_id": str(user_id),
            "certification_id": str(cert.certification_id),
            "cycle_id": str(cycle.cycle_id),
            "cycle_number": cycle_number,
            "issued_date": str(today),
            "valid_until": str(valid_until),
        }
