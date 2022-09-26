import simplejson as json
import sys
import time

file_name = 'whitelist.json.local'


class User:
    def __str__(self):
        return (', '.join([self.nick, self.PhoneNumber]))

    def for_json(self):
        result = self.__dict__.copy()
        result = {key: value
                  for key, value in result.items() if value is not None}
        return result


def write_to_file(data):
    json_data = json.dumps(data, indent=2, for_json=True)
    with open(file_name, "w") as file:
        file.write(json_data)


def read_user_data():
    with open(file_name, "r") as file:
        return json.load(file)


def verify_phone_number(phone):
    return phone.startswith('+') \
        and len(phone) == 13 \
        and phone[1:len(phone)].isnumeric()


def is_phone_number_on_list(phone):
    for user in read_user_data():
        if user['PhoneNumber'] == phone:
            return True


def create_user():
    print('Welcome to the fantastic door user creation wizard! Please enter information for the new user:')
    user = User()
    user.nick = input('  nick: ')
    user.PhoneNumber = input('  phone number: ')

    if is_phone_number_on_list(user.PhoneNumber):
        verify = input('WARNING: phone number is already on the list, continue anyway [y/n]?: ')
        if not verify.lower() == 'y':
            return None

    if not verify_phone_number(user.PhoneNumber):
        verify = input('WARNING: phone number format not recognized (must be in international format), continue anyway [y/n]?: ')
        if not verify.lower() == 'y':
            return None

    verify = input(f'Create user: {user} [y/n]?: ')

    if verify.lower() == 'y':
        user.uid = str(int(time.time()))
        return user
    else:
        return None


users = read_user_data()
new_user = create_user()

if new_user is not None:
    try:
        users.append(new_user)
        write_to_file(users)
        print('User created')
    except:
        print(f'An error occurred, please contact some nerd! {sys.exc_info()[0]}')
else:
    print('Canceled')
