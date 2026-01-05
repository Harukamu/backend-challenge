from fastapi import FastAPI
from app.api import processor_events, payouts, restaurants

app = FastAPI()

app.include_router(processor_events.router)
app.include_router(payouts.router)
app.include_router(restaurants.router)
