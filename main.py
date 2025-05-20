from NetSDK.NetSDK import NetClient
from NetSDK.SDK_Callback import fDisConnect, fHaveReConnect
from NetSDK.SDK_Enum import *
from NetSDK.SDK_Struct import *
from ctypes import *
import time
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def face_recognition_callback(lAnalyzerHandle, dwAlarmType, pAlarmInfo, pBuffer, dwBufSize, dwUser, nSequence, reserved):
    print(f"Alarm type: {dwAlarmType}")
    print("dwUser: ", dwUser)
    if dwAlarmType == EM_EVENT_IVS_TYPE.ACCESS_CTL:
        
        alarm_info = cast(pAlarmInfo, POINTER(DEV_EVENT_ACCESS_CTL_INFO)).contents
        
        # Print basic event information
        print("\n=== Face Recognition Event Detected ===")
        print(f"Time: {alarm_info.UTC.dwYear}-{alarm_info.UTC.dwMonth}-{alarm_info.UTC.dwDay} "
              f"{alarm_info.UTC.dwHour}:{alarm_info.UTC.dwMinute}:{alarm_info.UTC.dwSecond}")
        
        # Print face data
        print("\nFace Information:")
        print(f"User id: {alarm_info.szUserID.decode('utf-8', errors='ignore')}")
        check_in_to_crm(alarm_info.szUserID.decode('utf-8', errors='ignore'))

def check_in_to_crm(user_id):
    url = os.getenv("CHECK_IN_URL")
    payload = json.dumps({
        "user_id": user_id
    })
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def main():
    # Initialize SDK
    sdk = NetClient()
    sdk.InitEx(None)
    
    # Login parameters
    ip = "192.168.100.43"  # Replace with your device IP
    port = 80       # Replace with your device port
    username = "admin" # Replace with your username
    password = "LA7312@TA" # Replace with your password
    
    # Login structure
    stuInParam = NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY()
    stuInParam.dwSize = sizeof(NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY)
    stuInParam.szIP = ip.encode()
    stuInParam.nPort = port
    stuInParam.szUserName = username.encode()
    stuInParam.szPassword = password.encode()
    stuInParam.emSpecCap = EM_LOGIN_SPAC_CAP_TYPE.TCP
    
    stuOutParam = NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY()
    stuOutParam.dwSize = sizeof(NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY)
    
    # Login to device
    loginID, deviceInfo, error_msg = sdk.LoginWithHighLevelSecurity(stuInParam, stuOutParam)
    
    if loginID != 0:
        print("Successfully logged in to device")
        
        # Set up callback
        callback_func = CB_FUNCTYPE(None, C_LLONG, C_DWORD, c_void_p, POINTER(c_ubyte), 
                                  C_DWORD, C_LDWORD, c_int, c_void_p)(face_recognition_callback)
        
        # Start listening for events on channel 0
        realloadID = sdk.RealLoadPictureEx(loginID, 0, EM_EVENT_IVS_TYPE.ALL, True, callback_func)
        
        if realloadID != 0:
            print("Successfully subscribed to face recognition events")
            print("Listening for events... (Press Ctrl+C to stop)")
            
            try:
                while True:
                    time.sleep(1)  # Keep the program running
            except KeyboardInterrupt:
                print("\nStopping event listener...")
                sdk.StopLoadPic(realloadID)
        else:
            print(f"Failed to subscribe to events: {sdk.GetLastErrorMessage()}")
    
        # Cleanup
        sdk.Logout(loginID)
    else:
        print(f"Login failed: {error_msg}")
    
    sdk.Cleanup()

if __name__ == "__main__":
    main()