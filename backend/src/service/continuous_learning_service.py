from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.exceptions import CustomException
from src.model.continuous_learning import ContinuousLearningClass
from src.model.enum import ProcessStatus
from src.model.moc import MocClass


class ContinuousLearningService:

    @staticmethod
    def toggle_continuous_learning(
        moc_id: UUID,
        upload_proof: bool | None,
        certification_proof: bool | None,
        db: Session,
    ) -> dict:
        moc: MocClass = db.execute(
            select(MocClass).where(MocClass.moc_id == moc_id, MocClass.is_deleted == False)  # noqa
        ).scalars().first()
        if not moc:
            raise CustomException.NotFoundError("MOC")

        cl: ContinuousLearningClass = moc.continuous_learning
        if not cl:
            raise CustomException.NotFoundError("Continuous Learning record for MOC")

        if upload_proof is not None:
            cl.upload_proof = upload_proof
        if certification_proof is not None:
            cl.certification_proof = certification_proof

        all_done = cl.upload_proof and cl.certification_proof
        cl.cl_status = ProcessStatus.COMPLETED if all_done else ProcessStatus.INCOMPLETE

        db.commit()
        db.refresh(cl)

        from src.service.moc_status_service import MocStatusService
        MocStatusService.recompute_moc_status(moc_id, db)

        return {
            "moc_id": str(moc_id),
            "upload_proof": cl.upload_proof,
            "certification_proof": cl.certification_proof,
            "cl_status": cl.cl_status.value,
        }
