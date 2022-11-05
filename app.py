import Adafruit_DHT
import RPi.GPIO as GPIO
import serial
from flask import Flask, render_template
from mfrc522 import SimpleMFRC522

arduino = serial.Serial('/dev/ttyUSB0', 57600)

app = Flask(__name__)

cartoes_rfid = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temperatura-umidade')
def temperatura_umidade():
    sensor = Adafruit_DHT.DHT11

    GPIO.setmode(GPIO.BOARD)
    
    pino_sensor = 23
    
    # Efetua a leitura do sensor
    umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor)
    
    GPIO.cleanup()
    # Caso leitura esteja ok, mostra os valores na tela
    if umid is not None and temp is not None:
        return render_template('temperatura-umidade.html', umid=umid, temp=temp, erro='')
        # return "Temperatura = {0:0.1f}  Umidade = {1:0.1f}n".format(temp, umid)
    else:
        # Mensagem de erro de comunicacao com o sensor
        return render_template('temperatura-umidade.html', umid='', temp='', erro='Falha ao ler dados do DHT11 !!!')

@app.route('/leitor-rfid')
def leitor_rfid():
    leitor = SimpleMFRC522()
    try:
        id, text = leitor.read()
    finally:
        GPIO.cleanup()
        return render_template('leitor-rfid.html', id=id, text=text)

@app.route('/sensor-infravermelho')
def sensor_infravermelho():
    GPIO.setmode(GPIO.BCM)

    GPIO_PIN = 4
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    if GPIO.input(GPIO_PIN) == True:
        retorno = 'Nenhum item a frente.'
    else:
        retorno = 'Encontrado um item a frente.'

    GPIO.cleanup()
    return render_template('sensor-infravermelho.html', retorno=retorno)

#Rotas de API (Ou seja, retornará apenas o JSON)
@app.route('/api/temperatura-umidade')
def api_temperatura_umidade():
    sensor = Adafruit_DHT.DHT11

    GPIO.setmode(GPIO.BOARD)
    
    pino_sensor = 23
    
    # Efetua a leitura do sensor
    umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor)
    
    GPIO.cleanup()
    
    return {
        'umidade': int(umid),
        'temperatura': int(temp)
    }

@app.route('/api/leitor-rfid')
def api_leitor_rfid():
    leitor = SimpleMFRC522()
    try:
        # id, text = leitor.read()
        id = 904171428764

    finally:
        GPIO.cleanup()
        retorno = True if id in cartoes_rfid else False
        return {
            'permitido': retorno
        }

@app.route('/api/cadastro/leitor-rfid')
def api_cadastro_leitor_rfid():
    leitor = SimpleMFRC522()
    try:
        # id, text = leitor.read()
        id = 904171428764

        if id not in cartoes_rfid:
            cartoes_rfid.append(id)
        else:
            GPIO.cleanup()
            return {
                'cadastro': False,
                'erro': "Cartão já existente."
            }

    finally:
        GPIO.cleanup()
        return {
            'cadastro': True
        }

@app.route('/api/sensor-infravermelho')
def api_sensor_infravermelho():
    GPIO.setmode(GPIO.BCM)

    GPIO_PIN = 4
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    if GPIO.input(GPIO_PIN) == True:
        retorno = False
    else:
        retorno = True

    GPIO.cleanup()
    return {
        'encontrado_item': retorno
    }

@app.route('/api/sensor-gas')
def sensor_gas():
    valor = str(arduino.readline())
    valorGas = valor.split()
    valorGas[0] = valorGas[0].replace("b'", "")
    return {
        'valorSensorGas': int(valorGas[0])
    }

@app.route('/api/sensor-voltagem')
def sensor_voltagem():
    valor = str(arduino.readline())
    valorGas = valor.split()
    return {
        'valorSensorVoltagem': int(valorGas[1])
    }

@app.route('/api/sensor-amperagem')
def sensor_amperagem():
    valor = str(arduino.readline())
    valorGas = valor.split()
    valorGas[2] = valorGas[2].replace("\\r\\n'", "")
    return {
        'valorSensorAmperagem': float(valorGas[2])
    }

if __name__ == "__main__":
    app.run("0.0.0.0",6969)