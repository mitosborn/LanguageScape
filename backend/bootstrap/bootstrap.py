from constants import DEFAULT_READ_CAPACITY_UNITS, DEFAULT_WRITE_CAPACITY_UNITS
from model.LangModel import LangModel
from model.Learnset import Learnset
from model.Translation import Translation
from model.User import User
from model.UserLearnsetProgress import UserLearnsetProgress
from model.UserTranslationProgress import UserTranslationProgress

TABLES = [Learnset, Translation, User, UserLearnsetProgress, UserTranslationProgress]


def create_table(table_cls: LangModel):
    if not table_cls.exists():
        table_cls.create_table(read_capacity_units=DEFAULT_READ_CAPACITY_UNITS, write_capacity_units=DEFAULT_WRITE_CAPACITY_UNITS, wait=True)


