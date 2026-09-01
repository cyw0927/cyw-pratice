from fastapi import APIRouter

from app.modules.battle.router import router as battle_router
from app.modules.daily_mission.router import router as daily_router
from app.modules.grading.router import router as grading_router
from app.modules.learning.router import router as learning_router

api_router = APIRouter()
api_router.include_router(learning_router)
api_router.include_router(daily_router)
api_router.include_router(battle_router)
api_router.include_router(grading_router)
