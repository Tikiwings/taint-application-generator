import sys
import os
import subprocess as sp

def usage():
    print("generateApp.py <app_Folder_Name>\n")
    sys.exit(1)

def initApp(appName):
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

    with open("./app/src/main/AndroidManifest.xml", "a+") as f:
        f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n\
<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\"\n\
    \tpackage=\"com.example.karl.myapplication\">\n\
\n\
    \t<application\n\
        \t\tandroid:label=\"Demo App\"\n\
        \t\tandroid:theme=\"@style/AppTheme\">\n\
\n\
        \t\t<activity android:name=\".MainActivity\">\n\
            \t\t\t<intent-filter>\n\
                \t\t\t\t\t<action android:name=\"android.intent.action.MAIN\" />\n\
                \t\t\t\t\t<category android:name=\"android.intent.category.LAUNCHER\" />\n\
            \t\t\t</intent-filter>\n\
        \t\t</activity>\n\
    \t</application>\n\
\n\
</manifest>\n")
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

def main():
    if len(sys.argv) < 2:
        print("No destination name given")
        usage()
    #print(sys.argv[1])
    appList = getAppList(sys.argv)

    sp.run(['mkdir', "-p", 'applications'])

    #in applcations folder
    os.chdir("applications")
    for app in appList:
        initApp(app)
        buildApp(app)

    sys.exit(0)

main()
