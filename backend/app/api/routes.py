from fastapi import APIRouter
from app.api import auth, users, patients, visits, test_catalog, test_orders, test_results, billing, imaging, audit

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(visits.router, prefix="/visits", tags=["visits"])
api_router.include_router(test_catalog.router, prefix="/test-catalog", tags=["test_catalog"])
api_router.include_router(test_orders.router, prefix="/test-orders", tags=["test_orders"])
api_router.include_router(test_results.router, prefix="/test-results", tags=["test_results"])
api_router.include_router(billing.router, prefix="/billing", tags=["billing"])
api_router.include_router(imaging.router, prefix="/imaging-studies", tags=["imaging"])
api_router.include_router(audit.router, prefix="/audit-logs", tags=["audit_logs"])
