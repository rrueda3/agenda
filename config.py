import os

class Config():
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_DATABASE_URI = os.getenv('Database_URL','postgresql://neondb_owner:npg_hDAix4fsk9ZV@ep-empty-sky-a2yjgk3q-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_BOOTSWATCH_THEME = 'journal'
    TOASTR_POSITION_CLASS = 'toast-top-center'
    TOASTR_PROGRESS_BAR = 'false'
    TOASTR_OPACITY = 'false'
    TOASTR_TIMEOUT = 40000
    TOASTR_EXTENDED_TIMEOUT = 0
    