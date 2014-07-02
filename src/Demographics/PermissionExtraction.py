'''
Created on Mar 31, 2012

@author: Billy Symon
'''
import MySQLdb as mdb
import sys

markets = ["appsapk", "fdroid", "slideme"]

permissions = ["ACCESS_CHECKIN_PROPERTIES",
               "ACCESS_COARSE_LOCATION",
               "ACCESS_FINE_LOCATION",
               "ACCESS_LOCATION_EXTRA_COMMANDS",
               "ACCESS_MOCK_LOCATION",
               "ACCESS_NETWORK_STATE",
               "ACCESS_SURFACE_FLINGER",
               "ACCESS_WIFI_STATE",
               "ACCOUNT_MANAGER",
               "ADD_VOICEMAIL",
               "AUTHENTICATE_ACCOUNTS",
               "BATTERY_STATS",
               "BIND_APPWIDGET",
               "BIND_DEVICE_ADMIN",
               "BIND_INPUT_METHOD",
               "BIND_NFC_SURFACE",
               "BIND_NOTIFICATION_LISTENER_SERVICE",
               "BIND_PRINT_SERVICE",
               "BIND_REMOTEVIEWS",
               "BIND_TEXT_SERVICE",
               "BIND_VPN_SERVICE",
               "BIND_WALLPAPER",
               "BLUETOOTH",
               "BLUETOOTH_ADMIN",
               "BLUETOOTH_PRIVILIGED",              
               "BRICK",
               "BROADCAST_PACKAGE_REMOVED",
               "BROADCAST_SMS",
               "BROADCAST_STICKY",
               "BROADCAST_WAP_PUSH",
               "CALL_PHONE",
               "CALL_PRIVILEGED",
               "CAMERA",
               "CAPTURE_AUDIO_OUTPUT",
               "CAPTURE_SECURE_VIDEO_OUTPUT",
               "CAPTURE_VIDEO_OUTPUT",
               "CHANGE_COMPONENT_ENABLED_STATE",
               "CHANGE_CONFIGURATION",
               "CHANGE_NETWORK_STATE",
               "CHANGE_WIFI_MULTICAST_STATE",
               "CHANGE_WIFI_STATE",
               "CLEAR_APP_CACHE",
               "CLEAR_APP_USER_DATA",
               "CONTROL_LOCATION_UPDATES",
               "DELETE_CACHE_FILES",
               "DELETE_PACKAGES",
               "DEVICE_POWER",
               "DIAGNOSTIC",
               "DISABLE_KEYGUARD",
               "DUMP",
               "EXPAND_STATUS_BAR",
               "FACTORY_TEST",
               "FLASHLIGHT",
               "FORCE_BACK",
               "GET_ACCOUNTS",
               "GET_PACKAGE_SIZE",
               "GET_TASKS",
               "GLOBAL_SEARCH",
               "HARDWARE_TEST",
               "INJECT_EVENTS",
               "INSTALL_LOCATION_PROVIDER",
               "INSTALL_PACAKGES",
               "INTERNAL_SYSTEM_WINDOW",
               "INTERNET",
               "KILL_BACKGROUND_PROCESSES",
               "LOCATION_HARDWARE",
               "MANAGE_ACCOUNTS",
               "MANAGE_APP_TOKENS",
               "MANAGE_DOCUMENTS",
               "MASTER_CLEAR",
               "MEDIA_CONTENT_CONTROL",
               "MODIFY_AUDIO_SETTINGS",
               "MODIFY_PHONE_STATE",
               "MOUNT_FORMAT_FILESYSTEMS",
               "MOUNT_UNMOUNT_FILESYSTEMS",
               "NFC",
               "PERSISTENT_ACTIVITY",
               "PROCESS_OUTGOING_CALLS",
               "READ_CALENDAR",
               "READ_CALL_LOG",
               "READ_CONTACTS",
               "READ_EXTERNAL_STORAGE",
               "READ_FRAME_BUFFER",
               "READ_HISTORY_BOOKMARKS",
               "READ_INPUT_STATE",
               "READ_LOGS",
               "READ_PHONE_STATE",
               "READ_PROFILE",
               "READ_SMS",
               "READ_SOCIAL_STREAM",
               "READ_SYNC_SETTINGS",
               "READ_SYNC_STATS",
               "READ_USER_DICTIONARY",
               "REBOOT",
               "RECEIVE_BOOT_COMPLETED",
               "RECEIVE_MMS",
               "RECEIVE_SMS",
               "RECEIVE_WAP_PUSH",
               "RECORD_AUDIO",
               "REORDER_TASKS",
               "RESTART_PACKAGES",
               "SEND_SMS",
               "SET_ACTIVITY_WATCHER",
               "SET_ALARM",
               "SET_ALWAYS_FINISH",
               "SET_ANIMATION_SCALE",
               "SET_DEBUG_APP",
               "SET_ORIENTATION",
               "SET_POINTER_SPEED",
               "SET_PREFERRED_APPLICATIONS",
               "SET_PROCESS_LIMIT",
               "SET_TIME",
               "SET_TIME_ZONE",
               "SET_WALLPAPER",
               "SET_WALLPAPER_HINTS",
               "SIGNAL_PERSISTENT_PROCESSES",
               "STATUS_BAR",
               "SUBSCRIBED_FEEDS_READ",
               "SUBSCRIBED_FEEDS_WRITE",
               "SYSTEM_ALERT_WINDOW",
               "TRANSMIT_IR",
               "UNINSTALL_SHORTCUT",
               "UPDATE_DEVICE_STATS",
               "USE_CREDENTIALS",
               "USE_SIP",
               "VIBRATE",
               "WAKE_LOCK",
               "WRITE_APN_SETTINGS",
               "WRITE_CALENDAR",
               "WRITE_CALL_LOG",
               "WRITE_CONTACTS",
               "WRITE_EXTERNAL_STORAGE",
               "WRITE_GSERVICES",
               "WRITE_HISTORY_BOOKMARKS",
               "WRITE_PROFILE",
               "WRITE_SECURE_SETTINGS",
               "WRITE_SETTINGS",
               "WRITE_SMS",
               "WRITE_SOCIAL_STREAM",
               "WRITE_SYNC_SETTINGS",
               "WRITE_USER_DICTIONARY"]

zeroValuePermissions =["ADD_VOICEMAIL",
                       "BIND_REMOTEVIEWS",
                       "BIND_TEXT_SERVICE",
                       "BIND_VPN_SERVICE",
                       "BRICK",
                       "BROADCAST_PACKAGE_REMOVED",
                       "DIAGNOSTIC",
                       "DUMP",
                       "FACTORY_TEST",
                       "FORCE_BACK",
                       "INSTALL_PACKAGES",
                       "READ_HISTORY_BOOKMARKS",
                       "READ_PROFILE",
                       "READ_SOCIAL_STREAM",
                       "REBOOT",
                       "SET_ALWAYS_FINISH",
                       "SET_DEBUG_APP",
                       "SET_POINTER_SPEED",
                       "SET_PROCESS_LIMIT",
                       "SIGNAL_PERSISTENT_PROCESSES",
                       "UPDATE_DEVICE_STATS",
                       "WRITE_APN_SETTINGS",
                       "WRITE_HISTORY_BOOKMARKS",
                       "WRITE_PROFILE",
                       "WRITE_SOCIAL_STREAM"]

def connect():
    host, username, password, db = readFile('C:\\apks\\db\\dem_db.txt')
    return mdb.connect(host, username, password, db);

def readFile(filePath):
    lines = tuple(open(filePath, 'r'))
    return lines[0].replace("\n", ""), lines[1].replace("\n", ""), lines[2].replace("\n", ""), lines[3].replace("\n", "")

def executeDBCommand(command):
    con = connect()
    try:
        with con:
            cur = con.cursor()
            cur.execute(command)
            value = cur.fetchone()
            return value[0]
    except mdb.Error, e:
        writeError(command + "Resulted in Error %d: %s" % (e.args[0],e.args[1]))
    except:
        writeError ("!!!!! Unexpected error:" + str(sys.exc_info()[0]) + " When Executing Command "+command)
    finally:
        if con:
            con.close()

def writeError(message):
    f = open("Data_Mining_log.txt", 'a')
    f.write(message+"\n")
    f.close()
    
def getRequestedPermissionCountByMarket(permission, market):
    return executeDBCommand("SELECT COUNT(*) FROM appinfo, permissions_requested WHERE appinfo.filename = permissions_requested.filename AND appinfo.market = \" "+market+"\" AND permissions_requested.permission = \" android.permission."+permission+"\"")

def getTotalRequestedPermissionCount(permission):
    return executeDBCommand("SELECT COUNT(*) FROM permissions_requested WHERE permission = \" android.permission."+permission+"\"")

"""for permission in permissions:
    print "~"*50
    print "Permission -> " + permission
    print "~"*50
    for market in markets:
        print market + " -> " + str(getRequestedPermissionCountByMarket(permission, market))
    print "TOTAL -> " + str(getTotalRequestedPermissionCount(permission))
    print "*"*50"""
    
for permission in permissions:
    f2 = open('permissions.csv','a')
    
    if getTotalRequestedPermissionCount(permission) != 0 and permission not in zeroValuePermissions:
        print permission
        print "TOTAL -> " + str(getTotalRequestedPermissionCount(permission))
        f2.write(permission + "," + str(getTotalRequestedPermissionCount(permission)) + "\n")
    f2.close() # you can omit in most cases as the destructor will call if
