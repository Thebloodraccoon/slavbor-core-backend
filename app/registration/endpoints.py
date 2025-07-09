from fastapi import APIRouter, HTTPException, Depends

from app.registration.schemas import (
    RegistrationRequest,
    RegistrationResponse,
    RegistrationsResponse
)
from app.registration.services import RegistrationService
from app.core.dependencies import RegistrationRepoDep, UserServiceDep, AdminUserDep

router = APIRouter()

@router.post("/", response_model=dict)
async def submit_application(
    data: RegistrationRequest,
    repo: RegistrationRepoDep,
    user_service: UserServiceDep,
):
    service = RegistrationService(repo, user_service)
    reg_id = await service.submit_application(data.dict())
    return {"registration_id": reg_id}


@router.post("/submit", dependencies=[Depends(AdminUserDep)])
async def approve_application(
    registration_id: str,
    repo: RegistrationRepoDep,
    user_service: UserServiceDep,
):
    service = RegistrationService(repo, user_service)
    await service.approve_application(registration_id)
    return {"detail": "Approved"}


@router.get("/", response_model=RegistrationsResponse, dependencies=[Depends(AdminUserDep)])
async def list_applications(
    repo: RegistrationRepoDep,
    skip: int = 0, limit: int = 50,
):
    items = await repo.list_applications(skip, limit)
    return RegistrationsResponse(total=len(items), items=items)


@router.get("/{registration_id}", response_model=RegistrationResponse, dependencies=[Depends(AdminUserDep)])
async def get_application(
    registration_id: str,
    repo: RegistrationRepoDep,
):
    app = await repo.get_application(registration_id)
    if not app:
        raise HTTPException(status_code=404, detail="Not found")
    return RegistrationResponse(**app, registration_id=registration_id)
