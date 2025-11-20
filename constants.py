"""Static data structures used throughout the Welcome24 bot."""

from __future__ import annotations

from typing import Any, Dict, List

VIDEO_PLACEHOLDER = "https://drive.google.com/uc?export=download&id=1lwLn4wRK3uicUFHDqk-pqUkGUBNidx4m"
FILE_PLACEHOLDER = "https://example.com/files/welcome24_placeholder.pdf"

STAGE_TEXTS: Dict[str, Dict[str, Any]] = {
    "stage_0": {
        "title": "Этап 0 — Приветствие",
        "text": (
            "Привет! Добро пожаловать в Welcome 24 — компанию, где агенты работают на лучших условиях, "
            "получают до 95% комиссии и могут стать акционерами. Перед стартом познакомимся и настроим твой профиль. "
            "После видео нажми кнопку, чтобы подтвердить просмотр."
        ),
        "buttons": [
            {"text": "Я посмотрел видео", "callback_data": "stage_0_video_done"},
        ],
    },
    "stage_1": {
        "title": "Этап 1 — Корпоративная культура",
        "text": (
            "В этом этапе ты узнаешь про философию Welcome 24, ценности команды и почему мы строим компанию без начальников. "
            "Посмотри видео, затем изучи документ с миссией и УТП, чтобы понимать основу экосистемы."
        ),
        "buttons": [
            {"text": "Я посмотрел видео", "callback_data": "stage_1_video_done"},
            {"text": "Я прочитал документ", "callback_data": "stage_1_doc_done"},
            {"text": "Перейти к этапу 2", "callback_data": "stage_1_complete"},
        ],
    },
    "stage_2": {
        "title": "Этап 2 — Инфраструктура Welcome 24",
        "text": (
            "Разбираемся с инфраструктурой: главный чат и тематические ветки, региональные сообщества, каналы, бот Welcome24_Team "
            "и платформа Welcome2Business. Посмотри видео и изучи навигацию, чтобы знать, где искать ответы."
        ),
        "buttons": [
            {"text": "Я посмотрел видео", "callback_data": "stage_2_video_done"},
            {"text": "Перейти к этапу 3", "callback_data": "stage_2_complete"},
        ],
    },
    "stage_3": {
        "title": "Этап 3 — Акционерство Welcome 24",
        "text": (
            "Узнаем, как работает акционерство: прочитай манифест и посмотри ролик про преимущества партнёрства. "
            "Это путь к совместному росту и возможности влиять на компанию."
        ),
        "buttons": [
            {"text": "Я посмотрел видео", "callback_data": "stage_3_video_done"},
            {"text": "Я прочитал манифест", "callback_data": "stage_3_doc_done"},
            {"text": "Перейти к этапу 4", "callback_data": "stage_3_complete"},
        ],
    },
    "stage_4": {
        "title": "Этап 4 — Доход и 7 уровней пассива",
        "text": (
            "Разбираем систему дохода: как выйти на 95% комиссии, что такое 7 уровней пассивного дохода и как приглашать партнёров. "
            "Смотри видео, изучи материалы и переходи к следующему шагу."
        ),
        "buttons": [
            {"text": "Я посмотрел видео", "callback_data": "stage_4_video_done"},
            {"text": "Я изучил материалы", "callback_data": "stage_4_doc_done"},
            {"text": "Перейти к этапу 5", "callback_data": "stage_4_complete"},
        ],
    },
    "stage_5": {
        "title": "Этап 5 — Подключение площадок и CRM",
        "text": (
            "Настраиваем рабочие инструменты: Циан, Авито, Домклик и CRM. После видео можешь запросить подключение площадок "
            "и получить гайд по рекламе."
        ),
        "buttons": [
            {"text": "Я посмотрел видео", "callback_data": "stage_5_video_done"},
            {"text": "Запросить подключение", "callback_data": "stage_5_request"},
            {"text": "Перейти к этапу 6", "callback_data": "stage_5_complete"},
        ],
    },
    "stage_6": {
        "title": "Этап 6 — Юридический департамент",
        "text": (
            "Познакомься с юридическим департаментом: юристы Welcome 24 сопровождают сделки от проверки до ключей, "
            "работают по ЭДО и гарантируют безопасность. Получи контакты и шаблоны документов."
        ),
        "buttons": [
            {"text": "Я посмотрел видео", "callback_data": "stage_6_video_done"},
            {"text": "Перейти к этапу 7", "callback_data": "stage_6_complete"},
        ],
    },
    "stage_7": {
        "title": "Этап 7 — Ипотечный департамент",
        "text": (
            "90% клиентов думают про ипотеку. Узнай, как брокеры Welcome 24 ускоряют одобрения, работают с банками и помогают тебе "
            "закрывать сделки. После видео получи контакты ипотечников."
        ),
        "buttons": [
            {"text": "Я посмотрел видео", "callback_data": "stage_7_video_done"},
            {"text": "Перейти к этапу 8", "callback_data": "stage_7_complete"},
        ],
    },
    "stage_8": {
        "title": "Этап 8 — Работа с новостройками",
        "text": (
            "Новостройки дают быстрый доход и высокий процент. Видео расскажет о форматах работы, координаторах и полезных регламентах. "
            "Ознакомься и двигайся дальше."
        ),
        "buttons": [
            {"text": "Я посмотрел видео", "callback_data": "stage_8_video_done"},
            {"text": "Перейти к этапу 9", "callback_data": "stage_8_complete"},
        ],
    },
    "stage_9": {
        "title": "Этап 9 — Маркетинг и личный бренд",
        "text": (
            "Маркетинг приносит входящие лиды. Мы даём брендбук, шаблоны, контент-план и курс «Медиарилтор». "
            "Посмотри видео и изучи материалы."
        ),
        "buttons": [
            {"text": "Я посмотрел видео", "callback_data": "stage_9_video_done"},
            {"text": "Перейти к этапу 10", "callback_data": "stage_9_complete"},
        ],
    },
    "stage_10": {
        "title": "Этап 10 — Обучение и Wellconf",
        "text": (
            "Здесь собраны вебинары, база знаний, чек-листы и форум Wellconf. Узнай, как подключиться к системе обучения и где лежат материалы."
        ),
        "buttons": [
            {"text": "Я посмотрел видео", "callback_data": "stage_10_video_done"},
            {"text": "Перейти к этапу 11", "callback_data": "stage_10_complete"},
        ],
    },
    "stage_11": {
        "title": "Этап 11 — Десятки роста и бонус",
        "text": (
            "Десятки роста — это мини-группы для дисциплины и поддержки. Посмотри видео, изучи памятку и напиши комьюнити-менеджеру, "
            "если хочешь присоединиться. После завершения получишь финальное поздравление и бонусный урок об офлайн-жизни Welcome 24."
        ),
        "buttons": [
            {"text": "Я посмотрел видео", "callback_data": "stage_11_video_done"},
            {"text": "Завершить онбординг", "callback_data": "stage_11_complete"},
        ],
    },
}

STAGE_VIDEO_URLS: Dict[str, str | None] = {
    stage_key: VIDEO_PLACEHOLDER for stage_key in STAGE_TEXTS
}

DEFAULT_STAGE_ORDER: List[str] = list(STAGE_TEXTS.keys())

BUTTONS: Dict[str, Any] = {
    "share_contact": {"text": "Поделиться контактом", "request_contact": True},
}

LISTING_MANAGER_CHAT_ID = -1003260548150

FINAL_CONGRATS_TEXT = (
    "Поздравляем! Ты прошёл все этапы онбординга Welcome 24. "
    "Теперь ты знаешь инфраструктуру, систему дохода, юридическую поддержку, ипотеку, новостройки, маркетинг, обучение и десятки роста.\n\n"
    "Загляни в финальный гайд: https://teletype.in/@w24/waHOCrZKF3O\n"
    "Бонусный урок про офлайн-жизнь команды скоро прилетит отдельным сообщением."
)

