from backend.app.config import settings as base_settings


class SettingsWrapper:
    def __init__(self, base_settings):
        self._base_settings = base_settings
        self.SECRET_KEY = getattr(base_settings, "jwt_secret", None) or getattr(
            base_settings, "SECRET_KEY", None
        )

    def __getattr__(self, item):
        return getattr(self._base_settings, item)


settings = SettingsWrapper(base_settings)
