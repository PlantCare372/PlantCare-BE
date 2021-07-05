from .crud_item import item
from .crud_user import user
from .crud_plant import plant
from .crud_user_plant import user_plant
from .crud_user_reminder import user_reminder

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
