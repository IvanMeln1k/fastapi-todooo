import datetime
import os
import re

from dotenv import load_dotenv


load_dotenv()


def str_to_time(time_str: str)->datetime.timedelta:
    regex = re.compile(r'((?P<days>\d+?)d)? ?((?P<hours>\d+?)h)? ?((?P<minutes>\d+?)m)? ?((?P<seconds>\d+?)s)?')
    time_dict = regex.match(time_str).groupdict()
    for key, value in time_dict.items():
        if value is None:
            time_dict[key] = 0
        else:
            time_dict[key] = int(time_dict[key])
    return datetime.timedelta(**time_dict)


DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


PASS_SALT = os.getenv("PASS_SALT")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")


EXP_ACCESS = str_to_time(os.getenv("EXP_ACCESS"))
EXP_EMAIL = str_to_time(os.getenv("EXP_EMAIL"))
EXP_REFRESH = str_to_time(os.getenv("EXP_REFRESH"))
