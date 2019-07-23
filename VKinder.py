import vk_api

def get_main_user_info(vk):
    response_info = vk.users.get(fields='interests,bdate,sex,city,home_town,music,movies,books,games')
    response_groups = vk.groups.get()
    print(response_info)
    print(response_groups)
    dict_info = dict(
        age_from=2018 - int(response_info[0]['bdate'].split('.')[2]),
        age_to=2022 - int(response_info[0]['bdate'].split('.')[2]),
        sex=int(response_info[0]['sex'])+1,
        city=response_info[0]['city']['id'],
        id_group=response_groups['items']
    )
    print(dict_info)
    search_pair(vk, dict_info)
    return dict_info

def search_pair(vk, dict_info):
    response_pair = vk.users.search(count=10, fields='interests,bdate,sex,city,home_town,music,movies,books,games')
    print(response_pair)

def main():
    # user_input_login = input('Для доступа к программе введите свой логин и пароль или q для выхода.\nЛогин (или номер телефона: ')
    # user_input_password = input('Пароль: ')
    scope = 'groups,auido,video'
    vk_session = vk_api.VkApi(login='89090680016', password='Cvoboda21', api_version='5.101', scope=scope)
    # vk_session = vk.api.VkApi(login=user_input_login, password=user_input_password, api_version='5.101', scope=scope)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
#     user_input_id = input('Введите ID или короткое имя пользователя: ')
    get_main_user_info(vk)

if __name__ == '__main__':
    main()

