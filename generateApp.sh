#!/usr/bin/
mkdir ${1}
cd ${1}
echo -ne '1\n1\n\n' | gradle init
echo "include ':app'" >> settings.gradle
echo "buildscript {

    repositories {
        google()
        jcenter()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:3.1.3'
    }
}

allprojects {
    repositories {
        google()
        jcenter()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}" >> build.gradle
mkdir app
echo "apply plugin: 'com.android.application'

android {
    compileSdkVersion 25
    defaultConfig {
        applicationId \"com.example.karl.myapplication\"
        minSdkVersion 16
        targetSdkVersion 25
        versionCode 1
        versionName \"1.0\"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}

dependencies {
    implementation 'com.android.support.constraint:constraint-layout:1.1.2'
    implementation 'com.android.support:appcompat-v7:25.3.1'
}
" >> ./app/build.gradle
mkdir ./app/src
mkdir ./app/src/main
mkdir ./app/src/main/res
mkdir ./app/src/main/res/values
echo "<resources>

    <!-- Base application theme. -->
    <style name=\"AppTheme\" parent=\"Theme.AppCompat.Light.NoActionBar\">
        <!-- Customize your theme here. -->
    </style>

</resources>" >> ./app/src/main/res/values/styles.xml
echo "<?xml version=\"1.0\" encoding=\"utf-8\"?>
<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\"
    package=\"com.example.karl.myapplication\">

    <application
        android:label=\"Demo App\"
        android:theme=\"@style/AppTheme\">

        <activity android:name=\".MainActivity\">
            <intent-filter>
                <action android:name=\"android.intent.action.MAIN\" />
                <category android:name=\"android.intent.category.LAUNCHER\" />
            </intent-filter>
        </activity>
    </application>

</manifest>
" >> ./app/src/main/AndroidManifest.xml
./gradlew build
open ./app/build/reports/lint-results.html
cd ..

