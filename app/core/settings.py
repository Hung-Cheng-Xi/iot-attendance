from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	app_name: str
	admin_email: str
	items_per_user: int
	enable_docs: bool

	postgres_user: str
	postgres_password: str
	postgres_host: str
	postgres_port: int
	postgres_db: str

	class Config:
		env_file = '.env'


settings = Settings()
