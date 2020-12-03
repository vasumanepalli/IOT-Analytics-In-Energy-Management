import time
import sys
import ibmiotf.application
import ibmiotf.device
import random

#Provide your IBM Watson Device Credentials
organization = "egsm4v"
deviceType = "raspberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "12345678"
# Initialize GPIO
def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()
# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
amp=0
volt=0
while True:
    
    List=[]
    Power=(amp*volt)
    units=(Power/1000)
    
    if(units>0 and units<=100):
        payAmount=units*2.96
        fixedcharge=30.00
    elif(units>100 and units<=300):
        payAmount=(100*2.96)+(units-100)*5.56
        fixedcharge=50.00
    elif(units>300 and units<=500):
        payAmount=(100*2.96)+(300-100)*5.56+(units-200)*9.16
        fixedcharge=50.00
    elif(units>500):
        payAmount=(100*2.96)+(300-100)*5.56+(500-300)*9.16+(units-500)*10.61
        fixedcharge=100.00
    else:
        fixedcharge=50.00
        payAmount=0
    
    Total= payAmount+fixedcharge
    Total= int(Total)
    List.append(Total)
    summation=0
    for i in List:
        summation=i+summation
    Total+=summation
    
    amp+=5
    volt+=5
    Total+=1
    data = { 'Current' : amp, 'Voltage': volt, 'Total' : Total }
    #print (data)
    def myOnPublishCallback():
        
        print ("Published Current = %s A" % amp, "Voltage = %s V" % volt,  "Total = Rs.%s " % Total, "to IBM Watson")
    success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not connected to IoTF")
    time.sleep(5)
    deviceCli.commandCallback = myCommandCallback
# Disconnect the device and application from the cloud
deviceCli.disconnect()

    





        
