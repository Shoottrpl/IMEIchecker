from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from constant import DialogMessages
from .states import RegisterSG, DeleteSG, ImeiSG
from .handlers import handle_input, add_user_id, del_user, check_imei

register = Dialog(
    Window(
        Const(DialogMessages.ENTER_USER_ID),
        TextInput(id="user_id", on_success=handle_input),
        state=RegisterSG.user_id,
    ),
    Window(
        Format("{error}", "error"),
        SwitchTo(
            text=Const(DialogMessages.TRY_AGAIN),
            id="try_again",
            state=RegisterSG.user_id,
            when="error",
        ),
        Const("Пользователь добавлен", when="success"),
        state=RegisterSG.token,
        getter=add_user_id,
    ),
)

delete = Dialog(
    Window(
        Const(DialogMessages.ENTER_USER_ID),
        TextInput(id="user_id", on_success=handle_input),
        state=DeleteSG.user_id,
    ),
    Window(
        Format("{error}", "error"),
        SwitchTo(
            text=Const(DialogMessages.TRY_AGAIN),
            id="try_again",
            state=DeleteSG.user_id,
            when="error",
        ),
        Const("Пользователь удален", when="success"),
        state=DeleteSG.result,
        getter=del_user,
    ),
)

check = Dialog(
    Window(
        Const(DialogMessages.ENTER_IMEI),
        TextInput(id="imei", on_success=handle_input),
        state=ImeiSG.imei,
    ),
    Window(
        Format("{result}", "result"),
        Format("{error}", "error"),
        SwitchTo(
            text=Const(DialogMessages.TRY_AGAIN),
            id="try_again",
            state=ImeiSG.imei,
            when="error",
        ),
        state=ImeiSG.result,
        getter=check_imei,
    ),
)
