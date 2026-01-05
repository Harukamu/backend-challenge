import asyncio
import json
import httpx
import argparse

API_URL = "http://localhost:8000/v1/processor/events"

async def load_events(file_path: str):
    async with httpx.AsyncClient() as client:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                event = json.loads(line)
                resp = await client.post(API_URL, json=event)
                print(resp.status_code, resp.json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to events.jsonl")
    args = parser.parse_args()
    asyncio.run(load_events(args.file))
