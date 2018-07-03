import sys
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
import pandas as pd
import serial
import time

dataset_perm_list = ["android.permission.BIND_WALLPAPER", "android.permission.FORCE_BACK", "android.permission.READ_CALENDAR", "android.permission.BODY_SENSORS", "android.permission.READ_SOCIAL_STREAM", "android.permission.READ_SYNC_STATS", "android.permission.INTERNET",
"android.permission.CHANGE_CONFIGURATION", "android.permission.BIND_DREAM_SERVICE", "android.permission.HARDWARE_TEST", "com.android.browser.permission.WRITE_HISTORY_BOOKMARKS", "com.android.launcher.permission.INSTALL_SHORTCUT", "android.permission.BIND_TV_INPUT",
"android.permission.BIND_VPN_SERVICE", "android.permission.BLUETOOTH_PRIVILEGED", "android.permission.WRITE_CALL_LOG", "android.permission.CHANGE_WIFI_MULTICAST_STATE", "android.permission.BIND_INPUT_METHOD", "android.permission.SET_TIME_ZONE", "android.permission.WRITE_SYNC_SETTINGS",
"android.permission.WRITE_GSERVICES", "android.permission.SET_ORIENTATION", "android.permission.BIND_DEVICE_ADMIN", "android.permission.MANAGE_DOCUMENTS", "android.permission.FORCE_STOP_PACKAGES", "android.permission.WRITE_SECURE_SETTINGS", "android.permission.CALL_PRIVILEGED",
"android.permission.MOUNT_FORMAT_FILESYSTEMS", "android.permission.SYSTEM_ALERT_WINDOW", "android.permission.ACCESS_LOCATION_EXTRA_COMMANDS", "android.permission.BRICK", "android.permission.DUMP", "android.permission.CHANGE_WIFI_STATE", "android.permission.RECORD_AUDIO",
"android.permission.MODIFY_PHONE_STATE", "android.permission.READ_PROFILE", "android.permission.ACCOUNT_MANAGER", "android.permission.SET_ANIMATION_SCALE", "android.permission.SET_PROCESS_LIMIT", "android.permission.CAPTURE_SECURE_VIDEO_OUTPUT", "android.permission.SET_PREFERRED_APPLICATIONS",
"android.permission.ACCESS_ALL_DOWNLOADS", "android.permission.SET_DEBUG_APP", "android.permission.STOP_APP_SWITCHES", "android.permission.BLUETOOTH", "android.permission.ACCESS_WIFI_STATE", "android.permission.SET_WALLPAPER_HINTS", "android.permission.BIND_NOTIFICATION_LISTENER_SERVICE",
"android.permission.MMS_SEND_OUTBOX_MSG", "android.permission.CONTROL_LOCATION_UPDATES", "android.permission.UPDATE_APP_OPS_STATS", "android.permission.REBOOT", "android.permission.BROADCAST_WAP_PUSH", "com.android.launcher3.permission.READ_SETTINGS", "android.permission.ACCESS_NETWORK_STATE",
"android.permission.STATUS_BAR", "android.permission.WRITE_USER_DICTIONARY", "com.android.browser.permission.READ_HISTORY_BOOKMARKS", "android.permission.BROADCAST_PACKAGE_REMOVED", "android.permission.RECEIVE_SMS", "android.permission.WRITE_CONTACTS", "android.permission.READ_CONTACTS",
"android.permission.BIND_APPWIDGET", "android.permission.SIGNAL_PERSISTENT_PROCESSES", "android.permission.INSTALL_LOCATION_PROVIDER", "android.permission.ACCESS_DOWNLOAD_MANAGER_ADVANCED", "android.permission.WRITE_SETTINGS", "android.permission.MASTER_CLEAR", "android.permission.READ_INPUT_STATE",
"android.permission.MANAGE_APP_TOKENS", "android.permission.BIND_REMOTEVIEWS", "com.android.email.permission.ACCESS_PROVIDER", "android.permission.BIND_VOICE_INTERACTION", "com.android.launcher.permission.WRITE_SETTINGS", "com.android.gallery3d.filtershow.permission.READ", "android.permission.BIND_PRINT_SERVICE",
"android.permission.MODIFY_AUDIO_SETTINGS", "android.permission.USE_SIP", "android.permission.WRITE_APN_SETTINGS", "android.permission.ACCESS_SURFACE_FLINGER", "android.permission.FACTORY_TEST", "android.permission.READ_LOGS", "android.permission.PROCESS_OUTGOING_CALLS", "android.permission.UPDATE_DEVICE_STATS",
"android.permission.SEND_DOWNLOAD_COMPLETED_INTENTS", "android.permission.WRITE_CALENDAR", "android.permission.NFC", "android.permission.MANAGE_ACCOUNTS", "android.permission.SEND_SMS", "android.permission.INTERACT_ACROSS_USERS_FULL", "android.permission.ACCESS_MOCK_LOCATION",
"android.permission.BIND_ACCESSIBILITY_SERVICE", "android.permission.CAPTURE_AUDIO_OUTPUT", "android.permission.WRITE_SMS", "android.permission.GET_TASKS", "android.permission.DELETE_PACKAGES", "android.permission.ACCESS_CHECKIN_PROPERTIES", "android.permission.SEND_RESPOND_VIA_MESSAGE",
"android.permission.MEDIA_CONTENT_CONTROL", "android.permission.DOWNLOAD_WITHOUT_NOTIFICATION", "android.permission.RECEIVE_BOOT_COMPLETED", "android.permission.VIBRATE", "android.permission.DIAGNOSTIC", "android.permission.WRITE_PROFILE", "android.permission.CALL_PHONE",
"android.permission.FLASHLIGHT", "android.permission.READ_PHONE_STATE", "android.permission.CHANGE_COMPONENT_ENABLED_STATE", "android.permission.CLEAR_APP_USER_DATA", "android.permission.BROADCAST_SMS", "android.permission.KILL_BACKGROUND_PROCESSES", "android.permission.READ_FRAME_BUFFER",
"android.permission.SUBSCRIBED_FEEDS_WRITE", "android.permission.CAMERA", "android.permission.RECEIVE_MMS", "android.permission.WAKE_LOCK", "android.permission.ACCESS_DOWNLOAD_MANAGER", "com.android.launcher3.permission.WRITE_SETTINGS", "android.permission.DELETE_CACHE_FILES",
"android.permission.RESTART_PACKAGES", "android.permission.GET_ACCOUNTS", "android.permission.SUBSCRIBED_FEEDS_READ", "android.permission.CHANGE_NETWORK_STATE", "android.permission.READ_SYNC_SETTINGS", "android.permission.DISABLE_KEYGUARD", "com.android.launcher.permission.UNINSTALL_SHORTCUT",
"android.permission.USE_CREDENTIALS", "android.permission.READ_USER_DICTIONARY", "android.permission.WRITE_MEDIA_STORAGE", "android.permission.ACCESS_COARSE_LOCATION", "com.android.email.permission.READ_ATTACHMENT", "android.permission.SET_POINTER_SPEED", "android.permission.BACKUP",
"android.permission.EXPAND_STATUS_BAR", "android.permission.BLUETOOTH_ADMIN", "android.permission.ACCESS_FINE_LOCATION", "android.permission.LOCATION_HARDWARE", "android.permission.PERSISTENT_ACTIVITY", "android.permission.REORDER_TASKS", "android.permission.BIND_TEXT_SERVICE",
"android.permission.DEVICE_POWER", "android.permission.SET_WALLPAPER", "android.permission.READ_CALL_LOG", "android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.GET_PACKAGE_SIZE", "android.permission.WRITE_SOCIAL_STREAM", "android.permission.READ_EXTERNAL_STORAGE",
"android.permission.INSTALL_PACKAGES", "android.permission.AUTHENTICATE_ACCOUNTS", "com.android.launcher.permission.READ_SETTINGS", "com.android.alarm.permission.SET_ALARM", "android.permission.INTERNAL_SYSTEM_WINDOW", "android.permission.CLEAR_APP_CACHE", "android.permission.CAPTURE_VIDEO_OUTPUT",
"android.permission.GET_TOP_ACTIVITY_INFO", "android.permission.INJECT_EVENTS", "android.permission.SET_ACTIVITY_WATCHER", "android.permission.READ_SMS", "android.permission.BATTERY_STATS", "android.permission.GLOBAL_SEARCH", "android.permission.BIND_NFC_SERVICE", "android.permission.PACKAGE_USAGE_STATS",
"android.permission.SET_ALWAYS_FINISH", "android.permission.ACCESS_DRM", "android.permission.BROADCAST_STICKY", "android.permission.MOUNT_UNMOUNT_FILESYSTEMS"]

micro_dataset_perm_list = ["android.permission.ACCESS_WIFI_STATE", "android.permission.READ_LOGS", "android.permission.CAMERA", "android.permission.READ_PHONE_STATE", "android.permission.CHANGE_NETWORK_STATE", "android.permission.READ_SMS", "android.permission.CHANGE_WIFI_STATE", "android.permission.RECEIVE_BOOT_COMPLETED", "android.permission.DISABLE_KEYGUARD",
"android.permission.RESTART_PACKAGES", "android.permission.GET_TASKS", "android.permission.SEND_SMS", "android.permission.INSTALL_PACKAGES", "android.permission.SET_WALLPAPER", "android.permission.READ_CALL_LOG", "android.permission.READ_CONTACTS", "android.permission.WRITE_APN_SETTINGS", "android.permission.READ_EXTERNAL_STORAGE", "android.permission.WRITE_CONTACTS",
"com.android.browser.permission.READ_HISTORY_BOOKMARKS", "android.permission.WRITE_SETTINGS"]


def getPermissions(filename):
    '''
    input: filename
    output: permission list compatible with dataset
    '''
    # global dataset_perm_list #taken from header of dataset
    global micro_dataset_perm_list  # taken from header of dataset

    if(filename[0] is not None):
        app = dvm.APK(filename[0])
        per = app.get_permissions()  # androguard func to get perms
        one_hot_perm_list = [None]*21  # hardcoded
        j = 0
        for i in micro_dataset_perm_list:
            if(i in per):
                one_hot_perm_list[j] = 1
            else:
                one_hot_perm_list[j] = 0
            j = j+1

        # print(one_hot_perm_list)

    return one_hot_perm_list


def getPersmissions_from_csv(csv_file):
    try:
        df = pd.read_csv(csv_file[0])
    except:
        print(csv_file)

    headers = list(df.columns.values)
    for dfi in headers:#converting to numerals
        df[dfi] = pd.to_numeric(df[dfi], errors='coerce')    

    #one_hot_perm_list = [None]*21 #hardcoded
    dfi = df[micro_dataset_perm_list] #selecting the columns from the list for inputs
    dfo = df[["type"]] #selecting the output
	
    input_perms = dfi.values
    type_list = dfo.values
	
    required_output = []
    for i in type_list:
        if (i == 0):
            required_output.append([1,0])
        elif (i == 1):
            required_output.append([0,1])
    return input_perms, required_output #permission and its corresponding type
        


def test_inp_vec_extractor(perm): #systest
    
    x = "float input[1]["+ str(len(perm)) +"] = {"
    for i in perm:
        x = x + str(i) + ','

    x = x[:-1]
    '''
    try:
        print(x[22:]+",malware")
    except:
        print("\n")
    '''
    x = x + "};"

    with open(sys.argv[3], 'w') as fh:           #header file output
        fh.write("{}\n".format(x)) 
    # print(perm)
    
def csv_test_inp(n):
    csv_file = sys.argv[2:]
    perms, output = getPersmissions_from_csv(csv_file)
    ''' 
    # to print the required values

    for i in range(len(perms)):
		print(perms[i]),
		print(output[i])
    '''
    test_inp_vec_extractor(perms[int(n)])
    with open(sys.argv[5], 'a') as fh:           # output type
        fh.write("{}\n".format((output[int(n)])[1]))     
	
def serial_communicator(): #serialtest
    ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=3)
    file = sys.argv[2:]
    perm = getPermissions(file)
    message = ""
    for p in perm:
        message = message + str(p) + ' '
    message = message[:-1]
    message = message + '\n'
    #print(message)    
    ser.write(message.encode('utf-8'))
    # ser.close()
    # with serial.Serial('/dev/ttyUSB1', 115200, timeout=3) as sp:
    line = ""
    flag = True
    # polling -- the only cause of delay
    while(flag):
        time.sleep(0.1)
        ser.write(message.encode('utf-8'))
        try:
            line = ser.read(40)
            flag = False
        except:
            line = ""
        if(len(line) < 30):
            flag = True

    out = line.split()
    benign = out[1].decode('utf-8')
    mal =  out[2].decode('utf-8')

    if(float(mal) < float(benign)):
        print("benign " + benign)
    else:
        print("malware "+ mal)

if(str(sys.argv[1]) == "serialtest"):
    serial_communicator()    #for showing demo
elif(str(sys.argv[1]) == "systest"):
    file = sys.argv[2:]                           # apk input
    perm = getPermissions(file)
    test_inp_vec_extractor(perm)    #for software testing
elif(str(sys.argv[1]) == "csvtest"):
	csv_test_inp(sys.argv[4])		#for calculating result

