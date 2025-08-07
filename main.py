#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Direction

ev3 = EV3Brick()

motor_esq = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_dir = Motor(Port.B, Direction.COUNTERCLOCKWISE)
ultra_esq = UltrasonicSensor(Port.S1)
ultra_dir = UltrasonicSensor(Port.S2)

# Estados
PARA = 0
ANDA_RETO = 1
GIRA_ESQ = 2
GIRA_DIR = 3

# Constantes
VELOCIDADE_MAX  = 1000
VELOCIDADE_GIRO = 300
DISTANCIA_MAXIMA  = 650 # Distância máxima para detectar um objeto (em mm)
DISTANCIA_COMBATE = 125 # Distância mínima para detectar um objeto (em mm) e levantamento do braço

def main():
    ev3.speaker.beep()
    estado = GIRA_DIR
    while True:
        estado = prox_estado(estado)
        
        if (estado == ANDA_RETO):
            moverRobo(VELOCIDADE_MAX, VELOCIDADE_MAX)
        elif (estado == GIRA_ESQ):
            moverRobo(VELOCIDADE_GIRO, -VELOCIDADE_GIRO)
        elif (estado == GIRA_DIR):
            moverRobo(-VELOCIDADE_GIRO, VELOCIDADE_GIRO)
        else:
            pararRobo()

def prox_estado(estado_atual):
    dist_esq = ultra_esq.distance()
    dist_dir = ultra_dir.distance()

    if (dist_esq < DISTANCIA_MAXIMA and dist_dir < DISTANCIA_MAXIMA):
        estado = ANDA_RETO
    elif (dist_esq < DISTANCIA_MAXIMA):
        print("ESQ")
        estado = GIRA_ESQ
    elif (dist_dir < DISTANCIA_MAXIMA):
        print("DIR")
        estado = GIRA_DIR
    else:
      estado = estado_atual

    return estado

def moverRobo(vel_esq, vel_dir):
    motor_esq.run(vel_esq)
    motor_dir.run(vel_dir)

def pararRobo():
    motor_esq.stop()
    motor_dir.stop()

main()