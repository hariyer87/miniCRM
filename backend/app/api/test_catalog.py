from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models import TestCatalog, User
from app.schemas.test_catalog import TestCatalogCreate, TestCatalogOut, TestCatalogUpdate
from app.services.audit import log_action

router = APIRouter()


@router.get("", response_model=list[TestCatalogOut])
def list_tests(db: Session = Depends(deps.get_db)):
    return db.query(TestCatalog).filter(TestCatalog.is_active == True).all()


@router.post("", response_model=TestCatalogOut, dependencies=[Depends(deps.require_admin)])
def create_test(test_in: TestCatalogCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.require_admin)):
    if db.query(TestCatalog).filter(TestCatalog.code == test_in.code).first():
        raise HTTPException(status_code=400, detail="Code already exists")
    test = TestCatalog(**test_in.dict())
    db.add(test)
    db.commit()
    db.refresh(test)
    log_action(db, "CREATE_TEST", "test_catalog", test.id, current_user.id, None)
    return test


@router.get("/{test_id}", response_model=TestCatalogOut)
def get_test(test_id: int, db: Session = Depends(deps.get_db)):
    test = db.query(TestCatalog).get(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test


@router.put("/{test_id}", response_model=TestCatalogOut, dependencies=[Depends(deps.require_admin)])
def update_test(test_id: int, test_in: TestCatalogUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.require_admin)):
    test = db.query(TestCatalog).get(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    for field, value in test_in.dict(exclude_unset=True).items():
        setattr(test, field, value)
    db.commit()
    db.refresh(test)
    log_action(db, "UPDATE_TEST", "test_catalog", test.id, current_user.id, None)
    return test


@router.patch("/{test_id}/deactivate", response_model=TestCatalogOut, dependencies=[Depends(deps.require_admin)])
def deactivate_test(test_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.require_admin)):
    test = db.query(TestCatalog).get(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    test.is_active = False
    db.commit()
    db.refresh(test)
    log_action(db, "DEACTIVATE_TEST", "test_catalog", test.id, current_user.id, None)
    return test
