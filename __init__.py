# Yandex music auth parameters
USER_LOGIN = ''
USER_PASS = ''

# Collection of user lists that could be included to other user lists.
# Dict of (str, List<str>). Key is user list name and value is a collection of user lists
# that could include tracks from this user list.
# For example, we have list 'dance' that could include tracks from 5 different artists. These artists also have their
# separate play lists. So, we can write: {'dance', ['artist1', 'artist2'...]}
ALLOWED_USER_SUBLISTS = {

}
