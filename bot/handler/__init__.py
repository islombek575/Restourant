from bot.dispatcher import dp
from bot.handler.back import back_router
from bot.handler.main_router import main_router

dp.include_routers(
    main_router, back_router
)