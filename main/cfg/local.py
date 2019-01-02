from main.cfg.config import _Config


class _LocalConfig(_Config):
    DEBUG = True


config = _LocalConfig
