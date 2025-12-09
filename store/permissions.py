def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_officer(user):
    return user.groups.filter(name='StoreOfficer').exists()
