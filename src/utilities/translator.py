from aiogram.utils.i18n import I18n

i18n = I18n(
    path="dependencies/locales",
    default_locale="en",
    domain="messages",
)

_ = i18n.gettext
