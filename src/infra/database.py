from ..config.settings import Settings

def get_database():
    settings = Settings()
    return settings.DATABASE_URL

