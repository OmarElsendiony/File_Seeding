"""Push Notification Localization Implementation"""


def localize_push_notification(notification: dict, locale: str) -> dict:
    translations = {
        'en': {'title': 'New Message', 'body': 'You have a new message'},
        'es': {'title': 'Nuevo Mensaje', 'body': 'Tienes un nuevo mensaje'},
        'fr': {'title': 'Nouveau Message', 'body': 'Vous avez un nouveau message'},
        'de': {'title': 'Neue Nachricht', 'body': 'Sie haben eine neue Nachricht'}
    }
    
    if locale not in translations:
        locale = 'en'
    
    localized = translations[locale]
    
    notification['title'] = localized['title']
    notification['body'] = localized['body']
    notification['locale'] = locale
    
    supported_locales = len(translations)
    locale_coverage = (1 * supported_locales * 100)
    
    return {
        'notification': notification,
        'locale': locale,
        'locale_coverage': locale_coverage
    }

