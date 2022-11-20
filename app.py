import os
import sys
# sys.path.insert(0, '/home/pi/Desktop/vasco-da-gama/dbo_schema')

import Adafruit_DHT
import RPi.GPIO as GPIO
import serial
from flask import Flask, render_template, request
from mfrc522 import SimpleMFRC522
from dbo_schema import db
from dbo_schema.db import get_db


arduino = serial.Serial('/dev/ttyUSB0', 57600)

app = Flask(__name__)

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'base.sqlite'),
)
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

app.debug = True
db.init_app(app)

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
@app.route('/api/temperatura-umidade', methods=['GET'])
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

@app.route('/api/leitor-rfid', methods=['GET'])
def api_leitor_rfid():
    leitor = SimpleMFRC522()
    try:
        numero_cartao, text = leitor.read()
        
        GPIO.cleanup()

        json = request.json
        usuarioId = json['usuarioId']

        db = get_db()

        cartao = db.execute(
            'SELECT * FROM cartao_rfid WHERE usuario_id=? and numero_cartao=?', (usuarioId,numero_cartao,)
        ).fetchone()


        retorno = True if cartao is not None else False

        return {
            'permitido': retorno
        }

    except:
        GPIO.cleanup()
        
        return {
            'permitido': False
        }

@app.route('/api/cadastro/leitor-rfid', methods=['POST'])
def api_cadastro_leitor_rfid():
    try:
        leitor = SimpleMFRC522()

        json = request.json
        usuarioId = json['usuarioId']

        db = get_db()

        
        numero_cartao, text = leitor.read()

        cartao = db.execute(
            'SELECT * FROM cartao_rfid WHERE usuario_id=? and numero_cartao=?', (usuarioId,numero_cartao,)
        ).fetchone()


        if cartao is None:
            
            db.execute(
                'insert into cartao_rfid (usuario_id, numero_cartao)'
                'values (?, ?)',
                (usuarioId, numero_cartao)
            )

            db.commit()

        else:
            GPIO.cleanup()
            return {
                'cadastro': False,
                'erro': "Cartão já existente."
            }
        
        return {
            'cadastro': True
        }

    except:
        GPIO.cleanup()
        return {
            'cadastro': False
        }

@app.route('/api/sensor-infravermelho', methods=['GET'])
def api_sensor_infravermelho():
    GPIO.cleanup()
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

@app.route('/api/sensor-gas', methods=['GET'])
def sensor_gas():
    valor = str(arduino.readline())
    valorGas = valor.split()
    valorGas[0] = valorGas[0].replace("b'", "")
    return {
        'valor': int(valorGas[0])
    }

@app.route('/api/sensor-voltagem', methods=['GET'])
def sensor_voltagem():
    valor = str(arduino.readline())
    valorGas = valor.split()
    
    #tratando o valor lido pelo sensor
    valorGas[1] = int(valorGas[1]) - 2
    valorGas[1] = 0 if valorGas[1] < 0 else valorGas[1]
    return {
        'valor': int(valorGas[1])
    }

@app.route('/api/sensor-amperagem', methods=['GET'])
def sensor_amperagem():
    valor = str(arduino.readline())
    valorGas = valor.split()
    valorGas[2] = valorGas[2].replace("\\r\\n'", "")
    return {
        'valor': float(valorGas[2])
    }

@app.route('/api/login', methods=['POST'])
def login():
    try:
        json = request.json
        login = json['login']
        senha = json['senha']
        
        db = get_db()

        usuario = db.execute(
            'SELECT * FROM usuario WHERE login=? and senha=?', (login,senha,)
        ).fetchone()

        if usuario is None:
            return {
                'sucesso': False,
                'erro': 'Login ou senha incorreta'
            }
        
        return {
            'id': usuario['id'],
            'nome': usuario['nome'],
            'email': usuario['email'],
        }

    except Exception as e:
        
        return {
            'sucesso': False
        }

@app.route('/api/criar-usuario', methods=['POST'])
def criar_usuario():
    
    try:
        json = request.json
        nome = json['nome']
        email = json['email']
        login = json['login']
        senha = json['senha']
        
        db = get_db()

        usuario = db.execute(
            'SELECT * FROM usuario WHERE email=? or login=?', (email,login,)
        ).fetchone()

        if usuario is not None:
            return {
                'sucesso': False,
                'erro': 'E-mail ou login já cadastrado.'
            }
        
        db.execute(
            'INSERT INTO usuario (nome, email, login, senha)'
            ' VALUES (?, ?, ?, ?)',
            (nome, email, login, senha)
        )

        db.commit()

        return {
            'sucesso': True
        }
    except Exception as e:
        
        return {
            'sucesso': False
        }

if __name__ == "__main__":
    app.run("0.0.0.0",6969)