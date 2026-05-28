
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.exceptions import CustomException
from src.model.enum import ProcessStatus
from src.model.licensure import LicensureClass
from src.model.moc import MocClass


class LicensureService:

    @staticmethod
    def toggle_licensure(
        moc_id: UUID,
        upload_license: bool | None,
        upload_moc: bool | None,
        upload_marksheet: bool | None,
        db: Session,
    ) -> dict:
        moc: MocClass = db.execute(
            select(MocClass).where(MocClass.moc_id == moc_id, MocClass.is_deleted == False)  # noqa
        ).scalars().first()
        if not moc:
            raise CustomException.NotFoundError("MOC")

        lic: LicensureClass = moc.licensure
        if not lic:
            raise CustomException.NotFoundError("Licensure record for MOC")

        if upload_license is not None:
            lic.upload_license = upload_license
        if upload_moc is not None:
            lic.upload_moc = upload_moc
        if upload_marksheet is not None:
            lic.upload_marksheet = upload_marksheet

        all_done = lic.upload_license and lic.upload_moc and lic.upload_marksheet
        lic.licensure_status = ProcessStatus.COMPLETED if all_done else ProcessStatus.INCOMPLETE

        db.commit()
        db.refresh(lic)

        from src.service.moc_status_service import MocStatusService
        MocStatusService.recompute_moc_status(moc_id, db)

        return {
            "moc_id": str(moc_id),
            "upload_license": lic.upload_license,
            "upload_moc": lic.upload_moc,
            "upload_marksheet": lic.upload_marksheet,
            "licensure_status": lic.licensure_status.value,
        }
