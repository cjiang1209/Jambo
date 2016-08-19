
def is_member(user, groupName):
    if user:
        return user.groups.filter(name=groupName).exists()
    else:
        return False

def is_instructor(user):
    return is_member(user, 'Instructor');

def is_student(user):
    return is_member(user, 'Student');

def is_administrator(user):
    return is_member(user, 'Administrator');