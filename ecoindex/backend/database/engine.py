from prisma import Prisma

prisma = Prisma()


async def is_database_online() -> bool:
    if prisma.is_connected():
        return {"database": True}

    return {"database": False}
