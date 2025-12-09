import shutil
from pathlib import Path
from typing import List
from datetime import datetime
import pydicom
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import ImagingStudy, Patient
from app.schemas.imaging import ImagingOut
from app.services.audit import log_action

settings = get_settings()


def scan_and_import(db: Session) -> List[ImagingStudy]:
    inbox = Path(settings.dicom_inbox_dir)
    archive = Path(settings.dicom_archive_dir)
    inbox.mkdir(parents=True, exist_ok=True)
    archive.mkdir(parents=True, exist_ok=True)
    imported: List[ImagingStudy] = []

    for dicom_path in inbox.glob("*.dcm"):
        ds = pydicom.dcmread(dicom_path)
        patient_name = getattr(ds, "PatientName", None)
        patient_id_tag = getattr(ds, "PatientID", None)
        study_uid = getattr(ds, "StudyInstanceUID", None)
        study_date_raw = getattr(ds, "StudyDate", None)
        modality = getattr(ds, "Modality", None)
        description = getattr(ds, "StudyDescription", None)

        patient = None
        if patient_id_tag:
            patient = db.query(Patient).filter(Patient.patient_code == str(patient_id_tag)).first()
        if not patient and patient_name:
            patient = db.query(Patient).filter(Patient.first_name.ilike(f"%{patient_name}")).first()

        study_date = None
        if study_date_raw:
            try:
                study_date = datetime.strptime(str(study_date_raw), "%Y%m%d").date()
            except Exception:
                study_date = None

        imaging = ImagingStudy(
            patient_id=patient.id if patient else None,
            study_uid=study_uid,
            modality=modality,
            study_date=study_date,
            description=description,
            dicom_file_path=str(dicom_path.resolve()),
            source_device="Canon Xario 200",
        )
        db.add(imaging)
        db.commit()
        db.refresh(imaging)
        imported.append(imaging)
        log_action(db, "IMPORT_DICOM", "imaging_study", imaging.id, None, f"Imported {dicom_path.name}")
        shutil.move(str(dicom_path), archive / dicom_path.name)
    return imported
