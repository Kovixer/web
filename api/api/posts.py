import time
import re
# import shutil

from api._func.mongodb import db
from api._error import ErrorInvalid, ErrorAccess, ErrorWrong, ErrorUpload
from api._func import reimg, get_user, check_params, next_id, load_image


# Add / edit

async def edit(this, **x):
    # Checking parameters

    # Edit
    if 'id' in x:
        check_params(x, (
            ('id', True, int),
            ('name', False, str),
            ('cont', False, str),
            ('cover', False, str),
            ('file', False, str),
            ('category', False, int),
            ('tags', False, list, str),
        ))

    # Add
    else:
        check_params(x, (
            ('name', True, str),
            ('cont', True, str),
            ('cover', False, str),
            ('file', False, str),
            ('category', False, int),
            ('tags', False, list, str),
        ))

    # Processed

    processed = False

    # Formation

    if 'id' in x:
        post = db['posts'].find_one({'id': x['id']})

        # Wrong ID
        if not post:
            raise ErrorWrong('id')

    else:
        post = {
            'id': next_id('posts'),
            'time': this.timestamp,
            'reactions': {
                'likes': [],
                'reposts': [],
                'comments': [],
                'views': [],
            },
        }

    # Change fields
    for field in ('name', 'category', 'tags'):
        if field in x:
            post[field] = x[field]

    ## Content
    if 'cont' in x:
        post_updated = reimg(x['cont'])

        if x['cont'] != post_updated:
            processed = True

        post['cont'] = post_updated

    ## Cover

    post['cover'] = 'posts/0.png'

    if 'cover' in x:
        try:
            file_type = x['file'].split('.')[-1]

        # Invalid file extension
        except:
            raise ErrorInvalid('file')

        try:
            link = load_image(x['cover'], file_type)
            post['cover'] = link

        # Error loading cover
        except:
            raise ErrorUpload('cover')

    ### Cover from the first image
    # try:
    #     img = re.search(
    #         '<img src="[^"]*">',
    #         post['cont']
    #     )[0].split('"')[1].split('/')[2]
    #     shutil.copyfile(
    #         '../data/load/{}'.format(img),
    #         '../data/load/posts/{}.{}'.format(post['id'], img.split('.')[-1])
    #     )
    # except:
    #     pass

    # Save
    db['posts'].save(post)

    # Response

    res = {
        'id': post['id'],
    }

    if processed:
        res['cont'] = post['cont']

    return res

# Get

async def get(this, **x):
    # Checking parameters

    check_params(x, (
        ('id', False, (int, list), int),
        ('category', False, int),
        ('count', False, int),
        ('offset', False, int),
        ('search', False, str),
        # ('language', False, (int, str)),
    ))

    # Condition formation

    process_single = False

    db_condition = {}

    if 'id' in x:
        if type(x['id']) == int:
            db_condition['id'] = x['id']

            process_single = True

        else:
            db_condition['id'] = {'$in': x['id']}

    # # Language

    # if 'language' in x:
    #     x['language'] = get_language(x['language'])
    # else:
    #     x['language'] = this.language

    # Get

    count = x['count'] if 'count' in x else None

    db_filter = {
        '_id': False,
        'id': True,
        'name': True,
        'cont': True, # !
        'reactions': True,
        'time': True,
        'geo': True, # !
    }

    if process_single:
        db_filter['cont'] = True

    if 'search' in x:
        db_filter['name'] = True
        db_filter['cont'] = True
        db_filter['tags'] = True

    posts = list(db['posts'].find(db_condition, db_filter).sort('time', -1))

    # Filter

    if 'search' in x and x['search']:
        x['search'] = x['search'].lower()
        i = 0

        while i < len(posts):
            cond_name = x['search'] not in posts[i]['name'].lower()
            # TODO: HTML tags
            cond_cont = x['search'] not in posts[i]['cont'].lower()
            cond_tags = all(
                x['search'] not in tag.lower()
                for tag in posts[i]['tags']
            ) if 'tags' in posts[i] else True

            if cond_name and cond_cont and cond_tags:
                del posts[i]
                continue

            i += 1

        for i in range(len(posts)):
            # del posts[i]['cont'] # !

            if 'tags' in posts[i]:
                del posts[i]['tags']

    offset = x['offset'] if 'offset' in x else 0
    last = offset+x['count'] if 'count' in x else None

    posts = posts[offset:last]

    # Processing

    for i in range(len(posts)):
        ## Cover

        if 'cover' in posts[i]:
            posts[i]['cover'] = '/load/opt/' + posts[i]['cover']

        else:
            ### Cover from the first image
            try:
                img = re.search(
                    '<img src="[^"]*">',
                    posts[i]['cont']
                )[0].split('"')[1].split('/')[-1]

                posts[i]['cover'] = '/load/opt/' + img
            except:
                pass

        ## Content
        if not process_single:
            posts[i]['cont'] = re.sub(
                '<[^>]*>',
                '',
                posts[i]['cont']
            ).replace('&nbsp;', ' ')

    # Response

    res = {
        'posts': posts,
    }

    return res

# Delete

async def delete(this, **x):
    # Checking parameters

    check_params(x, (
        ('id', True, int),
    ))

    # Get

    post = db['posts'].find_one({'id': x['id']})

    ## Wrong ID
    if not post:
        raise ErrorWrong('id')

    # Delete

    db['posts'].remove(post)
