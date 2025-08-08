#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick # type: ignore
from pybricks.ev3devices import Motor, UltrasonicSensor, InfraredSensor # type: ignore
from pybricks.parameters import Port, Stop, Direction  # type: ignore
from time import sleep
from pybricks.tools import wait # type: ignore

class Enum():
    """
    A simple (and fallible) substitute for the enum.Enum class
    """
    def __init__(self, cls_name, items):
        if type(items) == dict:
            names = items.keys()
            vals  = items.values()
        else:
            names = items
            vals  = range(len(items))
        
        self.name_str_list = names
        self.constant_map = dict(zip(names, vals))
        self.name_str_map = dict(zip(vals, names))


    def __getattr__(self, name):
        return self.constant_map[name]
    
    def __getitem__(self, item):
        return self.constant_map[item]
    def __call__(self, num):
        return self.name_str_map[num]
    
    def __iter__(self):
        yield from self.name_str_list

    def __contains__(self, val):
        return (val in self.constant_map or
                val in self.name_str_map)

    def __len__(self):
        return len(self.constant_map)

#Estados
estado = Enum("Estado", ["ANDA_RETO", "GIRA"])

ANDA_RETO = estado.ANDA_RETO
GIRA = estado.GIRA


ev3 = EV3Brick()

motor_esq = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_dir = Motor(Port.B, Direction.COUNTERCLOCKWISE)
infra = InfraredSensor(Port.S2)


# Constantes
VELOCIDADE_MAX  = 100 # 100Velocidade maxima
VELOCIDADE_GIRO = 45
DISTANCIA_MAXIMA  = 80 # Distância máxima para detectar um objeto (em %): 0 -> 100


def main():
#    ev3.speaker.beep()
    estado = GIRA
    while True:
        estado = prox_estado(estado)
        if (estado == ANDA_RETO):
            moverRoboDc(VELOCIDADE_MAX, VELOCIDADE_MAX)
        elif (estado == GIRA):
            moverRoboDc(VELOCIDADE_GIRO, -VELOCIDADE_GIRO)
        else:
            pararRobo()
        sleep(0.05)

def prox_estado(estado_atual):
    distancia = infra.distance()
    if distancia <= DISTANCIA_MAXIMA:
        ev3.speaker.beep()
        return ANDA_RETO
    else:
        return GIRA

def moverRoboDc(vel_esq, vel_dir):
    motor_esq.dc(vel_esq)
    motor_dir.dc(vel_dir)

def moverRobo(vel_esq, vel_dir):
    motor_esq.run(vel_esq)
    motor_dir.run(vel_dir)

def pararRobo():
    motor_esq.stop()
    motor_dir.stop()

main()