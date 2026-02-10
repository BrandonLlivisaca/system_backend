from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED
from yaml import serialize

from app.database import get_db
from app.models.persona import TipoPersona
from app.models.user import User
from app.schemas.persona import PersonaCreate, PersonaUpdate, PersonaResponse, PersonaList
from app.services.persona_service import PersonaService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/persona", tags=["persona"])

@router.post("/create", response_model=PersonaResponse, status_code=HTTP_201_CREATED)
async def create_person(
        data: PersonaCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    """Create a new person"""
    service = PersonaService(db)

    try:
        persona = await service.create_persona(data)
        return persona
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=PersonaList)
async def list_persons(skip: int = Query(0, ge=0),
                       limit: int = Query(10, ge= 1, le=100),
                       tipo: TipoPersona | None = None,
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    """List all persons"""
    service = PersonaService(db)

    persona = await service.get_person_list(skip=skip, limit=limit, tipo=tipo)
    total = await service.count_persons()

    return {
        "personas": persona,
        "total": total,
        "page": (skip // limit) + 1,
        "per_page": limit
    }

@router.get("/{persona_id}", response_model=PersonaResponse)
async def get_person(persona_id: int, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    """Get a person for id"""
    service = PersonaService(db)

    persona = await service.get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Person not found")

    return persona

@router.put("/{persona_id}", response_model=PersonaResponse)
async def update_person(persona_id: int, data: PersonaUpdate, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """Update a person"""
    service = PersonaService(db)
    persona = await service.get_persona(persona_id)

    try:
        persona = await service.update_persona(persona_id, data)
        if not persona:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Person with id {persona_id} not found")

        return persona
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))

@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person(persona_id: int, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """Delete a person"""
    service = PersonaService(db)
    persona = await service.delete_person(persona_id)
    if not persona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Person not found")

    return None