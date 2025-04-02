from .admin_commands import router as admin_router
from .user_commands import router as user_router


routers = [admin_router, user_router]
