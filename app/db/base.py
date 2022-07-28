# Import all the models, so that Base has them before being
# imported by Alembic
from app.auth.models import Scope, User, UserScope
from app.universities.models import Building, Position, Room, University

from .base_class import Base
