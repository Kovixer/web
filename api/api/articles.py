import time

from mongodb import db
from api._error import ErrorInvalid, ErrorAccess
from api._func import reimg, get_user, check_params


# Получение

def get(this, **x):
	# Проверка параметров

	check_params(x, (
		('id', False, (int, list, tuple), int),
		('count', False, int),
		('category', False, int),
		('language', False, (int, str)),
	))

	# Список постов

	db_condition = {}

	if 'id' in x:
		if type(x['id']) == int:
			db_condition['id'] = x['id']
		
		else:
			db_condition['id'] = {'$in': x['id']}

	# # Язык

	# if 'language' in x:
	# 	x['language'] = get_language(x['language'])
	# else:
	# 	x['language'] = this.language

	# Получение постов

	count = x['count'] if 'count' in x else None

	db_filter = {
		'_id': False,
		'name': True,
		'cont': True,
	}

	posts = db['articles'].find(db_condition, db_filter)[:count]

	###

	res = {
		'articles': [{
			'name': post['name'],
			'cont': post['cont'],
			'tags': ['Программирование', 'Маркетинг'],
		} for post in posts]
	}

	return res

# Создание / редактирование

def edit(this, **x):
	post = db['articles'].find_one({'id': 1})

	post['cont'] = x['cont']

	db['articles'].save(post)