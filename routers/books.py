from fastapi import HTTPException,APIRouter
from schemas import BookCreate,BookResponse

router=APIRouter(
    preflix="/books",
    tags=[books],
)

@router.get