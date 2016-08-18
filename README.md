# Lewatoto_Python_LCD_Intel_Galileo
Adaptación de la librería [Adafruit_CharLCD.py][ada] para utilizar un display LCD con python y la librería [mraa][fa1ebf5e] de
Intel, en la placa de desarrollo Intel Galileo Gen 1 y 2.

## **work in progress**

## Conexiones por defecto
LCD|Intel Galileo pin|  
---|-----------------|
RS |2                 
E  |3                
D4 |4                
D5 |5                
D6 |6                
D7 |7                

## Conexiones definidas por el usuario
``` python
Import Lewatoto_CharLCD as LCD
rs = 2
en = 3
d4 = 4
d5 = 5
d6 = 6
d7 = 7
lcd = LCD.Lewatoto_CharLCD(rs, en, [d7, d6, d5, d4])
```
## v0.1.0
- Iniciar la LCD con pines por defecto o seleccionados por el usuario.
- LCD de columnas y filas definidas por el usuario.
- Modo 4 bits.
- Borrar el display.
- Mover cursor a inicio.

## Cosas por hacer
- [x] Iniciar la LCD.
- [ ] Mover cursor a posición indicada.
- [ ] Otros efectos/comandos.
- [ ] Agregar ejemplos.
- [ ] Crear el instalador.

[fa1ebf5e]: https://github.com/intel-iot-devkit/mraa "mraa"
[ada]: https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/blob/legacy/Adafruit_CharLCD/Adafruit_CharLCD.py "Adafruit_CharLCD"
