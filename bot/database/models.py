from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from bot.database.utils import CreatedModel

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/restourant")

session = sessionmaker(engine)()


class Base(DeclarativeBase):
    pass


class Category(CreatedModel):
    __tablename__ = "categories"
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str]

class Product(CreatedModel):
    __tablename__ = "products"
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str]
    description: Mapped[str]
    photo : Mapped[str]
    category_id : Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="cascade"))

metadata = Base.metadata

