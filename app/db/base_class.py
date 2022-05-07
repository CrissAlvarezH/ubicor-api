from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import declarative_base

# @as_declarative()
# class Base:
#     __name__: str

#     @declared_attr
#     def __tablename__(cls) -> str:
#         # generate __tablename__ automatically
#         return cls.__name__.lower()

Base = declarative_base()
