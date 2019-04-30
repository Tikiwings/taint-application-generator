import sys
import os
import subprocess as sp
import random as rand

def usage():
    print("generateApp.py <app_Folder_Name> ...\n")
    sys.exit(1)

#generate a list of random permissions an app will need to request
def randomizePermissions():
    appPermissions = {
        "normal"        :   [],
        "signature"     :   [],
        "dangerous"     :   []}

    normalPermissions = [
        "ACCESS_LOCATION_EXTRA_COMMANDS",
        "ACCESS_NETWORK_STATE",
        "ACCESS_NOTIFICATION_POLICY",
        "ACCESS_WIFI_STATE",
        "BLUETOOTH",
        "BLUETOOTH_ADMIN",
        "BLUETOOTH_STICKY",
        "CHANGE_NETWORK_STATE",
        "CHANGE_WIFI_MULTICAST_STATE",
        "CHANGE_WIFI_STATE",
        "DISABLE_KEYGUARD",
        "EXPAND_STATUS_BAR",
        "FOREGROUND_SERVICE",
        "GET_PACKAGE_SIZE",
        "INSTALL_SHORTCUT",
        "INTERNET",
        "KILL_BACKGROUND_PROCESSES",
        "MANAGE_OWN_CALLS",
        "MODIFY_AUDIO_SETTINGS",
        "NFC",
        "READ_SYNC_SETTINGS",
        "READ_SYNC_STATS",
        "RECEIVE_BOOT_COMPLETED",
        "REORDER_TASKS",
        "REQUEST_COMPANION_RUN_BACKGROUND",
        "REQUEST_COMPANION_USE_DATA_IN_BACKGROUND",
        "REQUEST_DELETE_PACKAGES",
        "REQUEST_IGNORE_BATTERY_OPTIMIZATIONS",
        "SET_ALARM",
        "SET_WALLPAPER",
        "SET_WALLPAPER_HINTS",
        "TRANSMIT_IR",
        "USE_FINGERPRINT",
        "VIBRATE",
        "WAKE_LOCK",
        "WRITE_SYNC_SETTINGS"]

    dangerPermissions = {
        "CALENDAR"      :   ["READ_CALENDAR", "WRITE_CALENDAR"],
        "CALL_LOG"      :   ["READ_CALL_LOG", "WRITE_CALL_LOG", "PROCESS_OUTGOING_CALLS"],
        "CAMERA"        :   ["CAMERA"],
        "CONTACTS"      :   ["READ_CONTACTS", "WRITE_CONTACTS", "GET_ACCOUNTS"],
        "LOCATION"      :   ["ACCESS_FINE_LOCATION", "ACCESS_COARSE_LOCATION"],
        "MICROPHONE"    :   ["RECORD_AUDIO"],
        "PHONE"         :   ["READ_PHONE_STATE", "READ_PHONE_NUMBERS", "CALL_PHONE", "ANSWER_PHONE_CALLS", "ADD_VOICEMAIL", "USE_SIP"],
        "SENSORS"       :   ["BODY_SENSORS"],
        "SMS"           :   ["SEND_SMS", "RECEIVE_SMS", "READ_SMS", "RECEIVE_WAP_PUSH", "RECEIVE_MMS"],
        "STORAGE"       :   ["READ_EXTERNAL_STORAGE", "READ_INTERNAL_STORAGE"]}


    normalPermissionCount = rand.randrange(len(normalPermissions))
    for _ in range(normalPermissionCount):
        appPermissions['normal'].append(rand.choice(normalPermissions))


    #TODO
    #implement ability to have multiple dangerous permissions for each app for 
    #interesting cross permission functionality
    #dangerPermissionCount = rand.randrange(len(dangerPermissions))
    dangerPermissionCount = 1
    for _ in range(dangerPermissionCount):
        pGroup = rand.choice(list( dangerPermissions ))
        perm = rand.choice(dangerPermissions[pGroup])
        appPermissions['dangerous'].append(perm)
    
    #remove dups
    appPermissions['normal'] = list(set(appPermissions['normal']))
    appPermissions['dangerous'] = list(set(appPermissions['dangerous']))
    
    return appPermissions    


def manifestPermissionStrings(permissionsList):
    permissions = ""

    for perm in permissionsList['normal']:
        permissions += f"<uses-permission android:name=\"android.permission.{perm}\"/>\n\t"

    for perm in permissionsList['dangerous']:
        permissions += f"<uses-permission android:name=\"android.permission.{perm}\"/>\n\t"
    return permissions


def initApp(appName, appPermissions):
    print("\033[1;31;40m ##################################")
    print("\033[1;31;40m ######## Initializing App ########")
    print("\033[1;31;40m ##################################")
    sp.run(["mkdir",  appName])
    os.chdir(appName)
    sp.run(['mkdir', 'app'])
    sp.run(['mkdir', 'app/src'])
    sp.run(['mkdir', 'app/src/main'])
    sp.run(['mkdir', 'app/src/main/res'])
    sp.run(['mkdir', 'app/src/main/res/values'])

    #in directory -> appName
    sp.run(["gradle", "init"], input='1\n1\n\n', encoding='ascii')
    with open("settings.gradle", "a+") as f:
        f.write("include ':app'\n")

    with open("build.gradle", "a+") as f:
        f.write("buildscript {\n\
\n\
    \trepositories {\n\
        \t\tgoogle()\n\
        \t\tjcenter()\n\
    \t}\n\
    \tdependencies {\n\
        \t\tclasspath 'com.android.tools.build:gradle:3.1.3'\n\
    \t}\n\
}\n\
\n\
allprojects {\n\
    \trepositories {\n\
        \t\tgoogle()\n\
        \t\tjcenter()\n\
    \t}\n\
}\n\
\n\
task clean(type: Delete) {\n\
    \tdelete rootProject.buildDir\n\
}")
        f.close()

    with open("./app/build.gradle", "a+") as f:
        f.write("apply plugin: 'com.android.application'\n\
\n\
android {\n\
    \tcompileSdkVersion 25\n\
    \tdefaultConfig {\n\
        \t\tapplicationId \"com.example.karl.myapplication\"\n\
        \t\tminSdkVersion 16\n\
        \t\ttargetSdkVersion 25\n\
        \t\tversionCode 1\n\
        \t\tversionName \"1.0\"\n\
    \t}\n\
    \tbuildTypes {\n\
        \t\trelease {\n\
            \t\t\tminifyEnabled false\n\
            \t\t\tproguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'\n\
        \t\t}\n\
    \t}\n\
}\n\
\n\
dependencies {\n\
    \timplementation 'com.android.support.constraint:constraint-layout:1.1.2'\n\
    \timplementation 'com.android.support:appcompat-v7:25.3.1'\n\
}\n")
        f.close()

    with open("./app/src/main/res/values/styles.xml", "a+") as f:
        f.write("<resources>\n\
\n\
    \t<!-- Base application theme. -->\n\
    \t<style name=\"AppTheme\" parent=\"Theme.AppCompat.Light.NoActionBar\">\n\
        \t\t<!-- Customize your theme here. -->\n\
    \t</style>\n\
\n\
</resources>")
        f.close()

    #APP MANIFEST
    #changed label from Demo App to name of application
    #added permissionsStr depending on which permissions are going to be required.
    #TODO change package name to involve appName
    with open("./app/src/main/AndroidManifest.xml", "a+") as f:
        f.write(f"""<?xml version=\"1.0\" encoding=\"utf-8\"?>
<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\"
    package=\"com.example.karl.myapplication\">

    {manifestPermissionStrings(appPermissions)}
    <application
        android:label=\"{appName}\"
        android:theme=\"@style/AppTheme\">

        <activity android:name=\".MainActivity\">
            <intent-filter>
                <action android:name=\"android.intent.action.MAIN\" />
                <category android:name=\"android.intent.category.LAUNCHER\" />
            </intent-filter>
        </activity>
    </application>

</manifest>""")
        f.close()

        #Java Main Activity File
        sp.run(["mkdir", "-p", "./app/src/main/java/com/example/karl/\
                myapplication"])
        with open("./app/src/main/java/com/example/karl/\
                myapplication/MainActivity.java", "a+") as f:
            f.write("""package com.example.karl.myapplication;

import android.app.Activity;
import android.os.Bundle;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}""")
            f.close()

        #Java Main Activity layout xml
        sp.run(["mkdir", "-p", "./app/src/main/res/layout"])
        with open("./app/src/main/res/layout/activity_main.xml", "a+") as f:
            f.write("""<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</android.support.constraint.ConstraintLayout>""")
            f.close()

        os.chdir("..")

        
def buildApp(appName):
    os.chdir(appName)
    print("\033[1;31;40m ##################################")
    print("\033[1;31;40m ########## Building App ##########")
    print("\033[1;31;40m ##################################")
    sp.run(['./gradlew', 'build'])
    sp.run(['open', './app/build/reports/lint-results.html'])
    os.chdir("..")


def getAppList(args):
    appList = []
    for i in range(1, len(args)):
        appList.append(args[i])
    return appList



def genDocumentation(appNames, appSettings):
    return None


def main():
    if len(sys.argv) < 2:
        print("No destination names given")
        usage()
    #print(sys.argv[1])
    appList = getAppList(sys.argv)

    sp.run(['mkdir', "-p", 'applications'])

    #in applcations folder
    os.chdir("applications")
    for app in appList:
        appPermissions = randomizePermissions()
        initApp(app, appPermissions)
        buildApp(app)

    sys.exit(0)

main()
