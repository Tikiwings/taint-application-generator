# taint-application-generator for new builds go into androidSDK/bin/sdkmanager --licenses and accept all licenses
Download gradle binary and set path to the gradle bin folder
Download Android SDK and set ANDROID_HOME env variable to the Android SDK bin folder

Make sure to allow debugging on the phone device in order to allow `gradlew build` command to work

Generated applications are stored in the applications folder

Multiple application names can be given and will generate all apps. Differing funcationality for all created apps has not been implemented yet
