# File for some tools


def get_command_input(user_input):
    return user_input.split(' ', 1)[1]
def string_is_int(string):
    try:
        a = int(string)
        return True
    except ValueError:
        return False
