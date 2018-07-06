# Results and Observations

Initially using 161 permissions provided by ADROIT dataset resulted in some form of overfitting ,which was overcome by reducing no of permission to 21 (22 was suggested by the paper, but dataset only had 21 of them). 




Table

Device | Execution time (us) | Clock | Power (Rough estimate)
--- | --- | --- | --- 
Intel® Core™ i7-4770 | 27.379 | 2.280 Ghz | ___
ARM Cortex™-A9 | 100.61 | 650 Mhz | 1.556 W 
Custom IP | 53.79 | 100 Mhz |0.238 W

Dataset Used :
For training and testing : ADROIT dataset { 8057 benignware samples and 3417 malware samples (skewed dataset) } 
                           https://github.com/alexMyG/ADROIT (They have their dataset and their code on this repo, awesome people)
                           
For Independent testing : Smaller dataset from Kaggle { 199 benignware and 198 malware }
                          https://www.kaggle.com/xwolf12/datasetandroidpermissions/home
                          
                          
Attributes choosen as per SigPID paper ( suggested by my friend ): 

"android.permission.ACCESS_WIFI_STATE", "android.permission.READ_LOGS", "android.permission.CAMERA", "android.permission.READ_PHONE_STATE", "android.permission.CHANGE_NETWORK_STATE", "android.permission.READ_SMS", "android.permission.CHANGE_WIFI_STATE", "android.permission.RECEIVE_BOOT_COMPLETED", "android.permission.DISABLE_KEYGUARD",
"android.permission.RESTART_PACKAGES", "android.permission.GET_TASKS", "android.permission.SEND_SMS", "android.permission.INSTALL_PACKAGES", "android.permission.SET_WALLPAPER", "android.permission.READ_CALL_LOG", "android.permission.READ_CONTACTS", "android.permission.WRITE_APN_SETTINGS", "android.permission.READ_EXTERNAL_STORAGE", "android.permission.WRITE_CONTACTS","com.android.browser.permission.READ_HISTORY_BOOKMARKS", "android.permission.WRITE_SETTINGS"


Classifier Used :
A simple Neural Network with an input layer,1 hidden layer and an output layer

Accuracy obtained after training with ADROIT dataset on test data with train_data:test_data split of 70:30 is 89.59%



# References
{Significant permission selection}
Sun, L., Li, Z., Yan, Q., Srisa-an, W., & Pan, Y. (2016, October). SigPID: significant permission identification for android malware detection. In Malicious and Unwanted Software (MALWARE), 2016 11th International Conference on (pp. 1-8). IEEE.

{Original train dataset}
Martín, A., Calleja, A., Menéndez, H. D., Tapiador, J., & Camacho, D. (2016, December). ADROIT: Android malware detection using meta-information. In Computational Intelligence (SSCI), 2016 IEEE Symposium Series on (pp. 1-8). IEEE. 

{Independent testing dataset}
"Urcuqui, C., & Navarro, A. (2016, April). Machine learning classifiers for android malware analysis. In Communications and Computing (COLCOM), 2016 IEEE Colombian Conference on (pp. 1-6). IEEE." 
