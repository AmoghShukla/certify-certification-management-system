from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.exceptions import CustomException
from src.model.enum import PaymentStatus
from src.model.moc import MocClass
from src.model.payment import PaymentClass
from src.model.user_examination_slot import UserExaminationSlotClass


class ExaminationPaymentService:

    @staticmethod
    def update_examination_payment(user_examination_slot_id: UUID, new_status: PaymentStatus, db: Session):
        booking: UserExaminationSlotClass = db.execute(
            select(UserExaminationSlotClass).where(
                UserExaminationSlotClass.user_examination_slot_id == user_examination_slot_id,
                UserExaminationSlotClass.is_deleted == False
            )
        ).scalars().first()

        if not booking:
            raise CustomException.NotFoundError("UserExaminationSlot")

        booking.payment_status = new_status
        db.commit()
        db.refresh(booking)

        return {
            "user_examination_slot_id": str(booking.user_examination_slot_id),
            "payment_status": booking.payment_status.value,
            "message": "Payment status updated successfully.",
        }


class MocPaymentService:

    @staticmethod
    def toggle_moc_payment_item(
        moc_id: UUID,
        portal_payment: bool | None,
        examination_payment: bool | None,
        certificate_payment: bool | None,
        db: Session,
    ) -> dict:
        moc: MocClass = db.execute(
            select(MocClass).where(
                MocClass.moc_id == moc_id,
                MocClass.is_deleted == False,  # noqa: E712
            )
        ).scalars().first()
        if not moc:
            raise CustomException.NotFoundError("MOC")

        payment: PaymentClass = moc.payment
        if not payment:
            raise CustomException.NotFoundError("Payment record for MOC")

        if portal_payment is not None:
            payment.portal_payment_status = portal_payment
        if examination_payment is not None:
            payment.examination_payment_status = examination_payment
        if certificate_payment is not None:
            payment.certificate_payment_status = certificate_payment

        all_done = (
            payment.portal_payment_status
            and payment.examination_payment_status
            and payment.certificate_payment_status
        )
        payment.payment_status = PaymentStatus.COMPLETED if all_done else PaymentStatus.PENDING

        db.commit()
        db.refresh(payment)

        # Recompute MOC status after any sub-change
        from src.service.moc_status_service import MocStatusService
        MocStatusService.recompute_moc_status(moc_id, db)

        return {
            "moc_id": str(moc_id),
            "portal_payment": payment.portal_payment_status,
            "examination_payment": payment.examination_payment_status,
            "certificate_payment": payment.certificate_payment_status,
            "payment_overall_status": payment.payment_status.value,
        }
