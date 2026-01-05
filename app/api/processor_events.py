from fastapi import APIRouter, HTTPException
from app.schemas.processor_event import ProcessorEventCreate, ProcessorEventResponse
from app.services.processor_events import process_event

router = APIRouter()

@router.post("/v1/processor/events", response_model=ProcessorEventResponse)
async def create_event(event: ProcessorEventCreate):
    """
    Ingest a processor event (idempotent)
    """
    try:
        result = await process_event(event)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))