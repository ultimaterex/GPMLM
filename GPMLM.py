from gmusicapi import Musicmanager
from gmusicapi import Mobileclient
import os.path
import sqlite3

mm = Musicmanager()
mc = Mobileclient()

pathToAuth = "./bin/auth.cred"
pathToAll_Songs = "./bin/all_songs.txt"
pathToAll_Playlists = "./bin/all_playlists.txt"
pathToConfig = "./bin/config.txt"


# This tries to get the the API key from GPM
def authenticate():
    try:
        Mobileclient.perform_oauth(pathToAuth, open_browser=True)
    except:
        print("An unknown Error has occurred, quitting setup")
        input("Press Enter to continue...")
        exit()


# This attempts to login using the API key, and then prints if it was successful
def login():
    login_state = False
    while not login_state:
        try:
            mc.oauth_login(device_id=Mobileclient.FROM_MAC_ADDRESS, oauth_credentials=pathToAuth, locale=u'en_US')
            if mc.is_authenticated():
                login_state = True
                print("Auth Success!")

        except OSError:
            print("Could not obtain MAC address, trying custom UID", )
            try:
                mc.oauth_login(device_id="0xDEADC1CADE111DAE", oauth_credentials=pathToAuth, locale=u'en_US')
                if mc.is_authenticated():
                    login_state = True
                    print("Auth Success!")
            except:
                break


# Checks the devices Registered to GPM
def devices():
    devices_registered = mc.get_registered_devices()
    print(devices_registered)
    for device in devices_registered:
        print(device)


# Returns all songs
def returnSongs():
    all_songs = mc.get_all_songs(incremental=False, include_deleted=None, updated_after=None)
    print(all_songs)
    if os.path.exists(pathToAll_Songs):
        os.remove(pathToAll_Songs)
    for item in all_songs:
        print(item)
        with open(pathToAll_Songs, "a", encoding='utf-8') as songs_file:
            songs_file.write("\n" + str(item))


# Returns all playlists
def returnPlaylists():
    all_playlists = mc.get_all_playlists(incremental=False, include_deleted=None, updated_after=None)
    print(all_playlists)
    if os.path.exists(pathToAll_Playlists):
        os.remove(pathToAll_Playlists)
    for item in all_playlists:
        print(item)
        with open(pathToAll_Playlists, "a", encoding='utf-8') as playlists_file:
            playlists_file.write("\n" + str(item))

# buffer text


# Program Starts here


# check if config file has been created, if not create a new one
if os.path.exists(pathToConfig):
    print("Loading previous config")
else:
    print("generating new config")
    with open("config.txt", 'a') as config_file:
        config_file.write("#\n"
                          "#GPMLM config \n"
                          "#\n")


# check if config file contains an api key token
with open(pathToConfig, "r") as file:
    config = file.read()


# check if InitialSetup flag is set to true and if api key exist, if not create both files
if "InitialSetup = True" in config and os.path.exists(pathToAuth):
    print("Skipping token setup")
else:
    print("Setting up token")
    # mm.perform_oauth()
    authenticate()
    with open("config.txt", 'a') as f:
        f.write("\nInitialSetup = True")
    print("Token has been setup successfully")


# login using existing token
print("Success!")
login()

# Checks to see if user has an active GPM Subscription
print(f"user has a active GPM Subscription: {mc.is_subscribed}")

# devices()
# returnSongs()
# returnPlaylists()

conn = sqlite3.connect('songs.db')





