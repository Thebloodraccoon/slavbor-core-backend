import json
from redis.asyncio import Redis

class RegistrationRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save_application(self, registration_id: str, data: dict):
        key = f"registration:{registration_id}"
        await self.redis.set(key, json.dumps(data), ex=30*24*60*60)
        await self.redis.sadd("registrations:pending", registration_id)
        await self.redis.set(f"registration:email:{data['email']}", registration_id)
        await self.redis.set(f"registration:username:{data['username']}", registration_id)

    async def get_application(self, registration_id: str) -> dict | None:
        key = f"registration:{registration_id}"
        value = await self.redis.get(key)
        return json.loads(value) if value else None

    async def list_applications(self, skip: int, limit: int) -> list[dict]:
        ids = await self.redis.smembers("registrations:pending")
        ids = list(ids)[skip : skip + limit]
        result = []
        for reg_id in ids:
            app = await self.get_application(reg_id)
            if app:
                app["registration_id"] = reg_id
                result.append(app)
        return result

    async def delete_application(self, registration_id: str):
        await self.redis.delete(f"registration:{registration_id}")
        await self.redis.delete(f"registration:email:{registration_id}")
        await self.redis.delete(f"registration:username:{registration_id}")
        await self.redis.srem("registrations:pending", registration_id)
