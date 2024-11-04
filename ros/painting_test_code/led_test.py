from fastapi import FastAPI
# GPIO library
import Jetson.GPIO as GPIO
 
app = FastAPI()

# LED 사용할 핀 정의
led_pin = 7
 
# GPIO 채널 설정
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW) 
 
@app.post("/paint/{switchStatus}")
def paintOnOff(switchStatus: str):
    if switchStatus == 'on' :
       GPIO.output(led_pin, GPIO.HIGH)
    elif switchStatus == 'off' :
       GPIO.output(led_pin, GPIO.LOW)
    else :
       
       return {"error": "Invalid operation"}
