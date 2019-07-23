import vk_api
import json


def define_search_criteria(vk):
    user_input_user = input('Введите id или имя пользователя в ВК для поиска пары: ')
    user_input_age_from = input('Введите нижнюю границу возраста для подбора пары: ')
    user_input_age_to = input('Введите верхнюю границу возраста для подбора пары: ')
    response_info = vk.users.get(user_ids=user_input_user, fields='sex,city')
    checked_info = check_user_data(vk, response_info)

    match_info = dict(
        age_from=user_input_age_from,
        age_to=user_input_age_to,
        sex=checked_info[0]['sex'],
        city=checked_info[0]['city']['id']
    )

    return match_info


def check_user_data(vk, info):

    if info[0]['sex'] == 0:
        user_input_sex = input('Введите пол пользователя, для которого подбирается пара:')
    else:
        user_input_sex = info[0]['sex']
    info[0]['sex'] = 2 if user_input_sex == 1 else 1

    if info[0].get('city', False) == False:
        user_input_country = input('Введите двухбуквенный код страны в стандарте ISO 3166-1 alpha-2, в которой проживает пользователь, для которого подбирается пара: ')
        response_country = vk.database.getCountries(need_all=0, code=user_input_country)
        user_input_city = input('Введите город проживания пользователя, для которого подбирается пара: ')
        response_city = vk.database.getCities(country_id=response_country['items'][0]['id'], q=user_input_city, count=1)
        info[0]['city'] = response_city['items'][0]

    return info


def search_pretender(vk, info):
    response_pretender = vk.users.search(
        count=10, fields='bdate,sex,city',
        age_from=info['age_from'], age_to=info['age_to'],
        sex=info['sex'], city=info['city']
    )
    return response_pretender


def get_top_3_avatars(vk, info):
    pretender_list = []
    for pretender in info['items']:
        response_photos = vk.photos.get(owner_id=pretender['id'], album_id='profile', extended=1)
        list_to_sort = response_photos['items']
        photo_list = sorted(list_to_sort, key=lambda x: x['likes']['count'], reverse=True)
        pretender = dict(id=pretender['id'], photos=[])
        for photo in photo_list[0:3]:
            pretender['photos'].append(photo['sizes'][-1]['url'])
        pretender_list.append(pretender)

    return json.dumps(pretender_list, ensure_ascii=False, indent=2)


def main():
    # user_input_login = input('Для доступа к программе введите свой логин и пароль или q для выхода.\nЛогин (или номер телефона: ')
    # user_input_password = input('Пароль: ')
    scope = 'photos,groups'
    vk_session = vk_api.VkApi(login='89090680016', password='', api_version='5.101', scope=scope)
    # vk_session = vk.api.VkApi(login=user_input_login, password=user_input_password, api_version='5.101', scope=scope)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    pretender_list = search_pretender(vk, define_search_criteria(vk))
    print(get_top_3_avatars(vk, pretender_list))

if __name__ == '__main__':
    main()

