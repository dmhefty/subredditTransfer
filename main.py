import requests
import praw
from pprint import pprint
from prawcore.exceptions import Forbidden, NotFound
import getpass

def main():
    print(
        '''To use this, both accounts must have a script application created for this at: https://www.reddit.com/prefs/apps/
    Passwords are intentionally obscured.
    ''')

    # Grab source user's info
    usernameUser1 = input('Source user\'s username: ')
    passwordUser1 = getpass.getpass(f'{usernameUser1}\'s password: ')
    personalIdUser1 = input(f'{usernameUser1}\'s application ID: ')
    secretIdUser1 = input(f'{usernameUser1}\'s secret application ID: ')

    # Authenticate source user
    redditUser1 = praw.Reddit(
        client_id= personalIdUser1,
        client_secret= secretIdUser1,
        password= passwordUser1,
        user_agent="subredditTransfer by " + usernameUser1,
        username= usernameUser1,
    )

    try:
        redditUser1.user.me() # Just grab username to ensure connection works
    except:
        print('Authentication failed. Retry input or check connection.')
        return

    print()

    # Grab destination user's info
    usernameUser2 = input('Destination user\'s username: ')
    passwordUser2 = getpass.getpass(f'{usernameUser2}\'s password: ')
    personalIdUser2 = input(f'{usernameUser2}\'s application ID: ')
    secretIdUser2 = input(f'{usernameUser2}\'s secret application ID: ')

    # Authenticate destination user
    redditUser2 = praw.Reddit(
        client_id= personalIdUser2,
        client_secret= secretIdUser2,
        password= passwordUser2,
        user_agent="subredditTransfer by " + usernameUser2,
        username= usernameUser2,
    )

    try:
        redditUser2.user.me() # Just grab username to ensure connection works
    except:
        print('Authentication failed. Retry input or check connection.')
        return

    print()

    # Grab the source user's subreddits
    subscribed1 = list(redditUser1.user.subreddits(limit=None))

    # Run through each and add it to the destination user's account
    unsubbed = list()
    print(f'u/{usernameUser2} subscribing to subs of user u/{usernameUser1}:')
    for sub in subscribed1:
        try:
            print(f'Subscribing to r/{sub}')
            redditUser2.subreddit(sub.display_name).subscribe()

        # Edge cases
        except Forbidden:
            print(f'Subreddit {sub} is private/quarantined/banned')
            unsubbed.append(sub)

        except NotFound:
            print(f'Subreddit {sub} cannot be found')
            unsubbed.append(sub)

    print(f'\nSubscritption complete! u/{usernameUser2} has subscribed to the subscriptions of u/{usernameUser1}')

    if unsubbed:
        print('Subsciption failed for the following subreddits: ')
        # I split this print out to look slightly nicer
        for sub in unsubbed[:-1]:
            print(sub, end=', ')
        print(unsubbed[-1])

if __name__ == '__main__':
    main()
