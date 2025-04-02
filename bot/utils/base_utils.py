import re

from typing import Optional, Dict


def is_valid_imei(imei: str) -> bool:
    """
    Проверка валидности передаваемого IMEI

    :param imei: Строка, представляющая IMEI
    :return: True если IMEI валиден, False если нет
    """
    if not re.match(r"^\d{15}$", imei):
        return False

    return check_luhn(imei)


def validate_user_id(user_id: str) -> Optional[Dict[str, str]]:
    """
    Проверка валидности ID пользователя

    :param user_id: ID пользователя
    :return: Словарь с ошибкой, если user_id невалиден, если все корректно None
    """
    if not user_id:
        return {
            "error": f"Передайте id пользователя: <code>/add &lt;user_id&gt;</code>"
        }

    if not user_id.isdigit():
        return {"error": "user_id должно быть числом."}

    if len(user_id) != 10:
        return {"error": "user_id должно быть 10 значным числом"}


def check_luhn(imei: str) -> bool:
    """
    Проверка контрольной суммы IMEI, по алгоритму Луна

    :param imei: Строка, представляющая IMEI
    :return: True, если контрольная сумма верна, False если нет
    """
    total = 0
    reverse_imei = imei[::-1]

    for i, digits in enumerate(reverse_imei):
        n = int(digits)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0


def template_imei_info(data: dict) -> str:
    """
    Форматирует информацию об устройстве, по шаблону.

    :param data: Словарь с информацией об устройстве
    :return: Шаблон строка
    """
    device_name = data.get("deviceName", None)
    image_url = data.get("image", None)
    serial_number = data.get("serial", None)
    purchase_date = data.get("purchase_date", None)
    purchase_country = data.get("purchaseCountry", None)
    block_status = data.get("usaBlockStatus", None)
    network = data.get("network", None)

    text = f"""\
            Информация об устройстве:
            \nНазвание устройства: {device_name}
            \nСсылка на изображение: [ссылка]({image_url}) 
            \nСерийный номер: {serial_number}
            \nДата покупки: {purchase_date}
            \nСтрана покупки: {purchase_country}
            \nСтатус блокировки: {block_status}
            \nСеть: {network}
            """

    return text
