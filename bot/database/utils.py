from datetime import datetime
from typing import Optional, List, Any

import pytz
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from sqlalchemy.orm import declared_attr

# Assume db and Base are imported from your db module
from bot.database import db, Base


# Initialize db (assuming this is sync; if async, adjust accordingly)

async def initialize_db():
    await db.init()
    await db.create_all()

# Timezone setup (portable with pytz)
TZ = pytz.timezone("Asia/Tashkent")


def get_current_time() -> datetime:
    return datetime.now(TZ)


# ----------------------------- ABSTRACT CLASS ----------------------------------
class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception as e:
            print(f"Commit failed: {e}")
            await db.rollback()
            raise

    @classmethod
    async def create(cls, **kwargs: Any) -> "AbstractClass":
        obj = cls(**kwargs)
        db.add(obj)
        await cls.commit()
        print(f"Created {cls.__name__} with id {obj.id}")
        return obj

    @classmethod
    async def update(cls, id_: int, **kwargs: Any) -> None:
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()
        print(f"Updated {cls.__name__} with id {id_}")

    @classmethod
    async def get(cls, id_: int) -> Optional["AbstractClass"]:
        query = select(cls).where(cls.id == id_)
        objects = await db.execute(query)
        obj = objects.first()
        return obj[0] if obj else None

    @classmethod
    async def get_with_id(cls, id__: str, id_: int) -> List["AbstractClass"]:
        field = getattr(cls, id__, None)
        if field is None:
            raise AttributeError(f"{id__} degan ustun mavjud emas.")
        query = select(cls).where(field == id_)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def delete(cls, id_: int) -> bool:
        query = sqlalchemy_delete(cls).where(cls.id == id_)
        result = await db.execute(query)
        if result.rowcount > 0:
            await cls.commit()
            print(f"Deleted {cls.__name__} with id {id_}")
            return True
        print(f"No {cls.__name__} found with id {id_} to delete")
        return False

    @classmethod
    async def delete_by_field(cls, field_name: str, value: Any) -> int:
        field = getattr(cls, field_name, None)
        if not field:
            raise ValueError(f"{cls.__name__} does not have field {field_name}")
        query = sqlalchemy_delete(cls).where(field == value)
        result = await db.execute(query)
        await cls.commit()
        print(f"Deleted {result.rowcount} {cls.__name__}(s) where {field_name} == {value}")
        return result.rowcount

    @classmethod
    async def get_all(cls, order_fields: List[str] = None) -> List["AbstractClass"]:
        query = select(cls)
        if order_fields:
            order_by = [getattr(cls, field) for field in order_fields if hasattr(cls, field)]
            query = query.order_by(*order_by)
        objects = await db.execute(query)
        return [row[0] for row in objects.all()]

    @classmethod
    async def exists(cls, id_: int) -> bool:
        """Check if an instance exists by ID."""
        query = select(cls.id).where(cls.id == id_)
        result = await db.execute(query)
        return result.scalar() is not None


# ----------------------------- BASE MODEL ----------------------------------
class CreatedModel(Base, AbstractClass):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    id = Column(Integer, primary_key=True, autoincrement=True)