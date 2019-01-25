import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User

def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    
    dates = []
    ages = []
    date = get_friends(user_id, 'bdate')
    
    if 8 <= len(date) <= 10:
        dates += date
    
    for i in dates:
        age = (dt.date.today - date)/365
        ages += age
    
    if len(ages) > 0:
        return median(ages)
    else:
        return None

    return age_predict(user_id)
