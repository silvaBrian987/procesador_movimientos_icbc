from datetime import date, datetime
import logging
import re
from prettytable import PrettyTable
import argparse

LOGGER: logging.Logger = logging.Logger(__name__)


class Movimiento():
    fecha: date
    detalle: str
    debito: float
    credito: float

    def __str__(self):
        return str([self.fecha, self.detalle, self.debito, self.credito])


def props(cls):
    return [i for i in cls.__dict__['__annotations__'].keys() if i[:1] != '_']


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        prog='Procesador de movimientos de caja de ahorro de ICBC')
    parser.add_argument(
        '-f', '--filter', action='append', help='Filtrar informacion por campo. Ej. -f detalle=PEPE')
    parser.add_argument('file', help='Archivo a procesar', metavar='FILE')

    args = parser.parse_args()

    movimientos: list[Movimiento] = []
    with open(args.file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            LOGGER.debug(line)
            fields = line.split(',')
            mov = Movimiento()
            fechaArr = fields[0].split('/')
            year = int(f"{str(datetime.now().year)[0:2]}{int(fechaArr[2])}")
            mov.fecha = date(day=int(fechaArr[1]), month=int(
                fechaArr[0]), year=year)
            mov.detalle = fields[1]
            mov.debito = float(fields[2])
            mov.credito = float(fields[3])
            movimientos.append(mov)

    # LOGGER.info(movimientos)
    table = PrettyTable(props(Movimiento))
    for mov in movimientos:
        if args.filter:
            ok = False
            for filter in args.filter:
                key, value = filter.split('=')
                if(value in str(mov.__dict__[key])):
                    ok = True
            if ok:
                table.add_row(mov.__dict__.values())
        else:
            table.add_row(mov.__dict__.values())
    print(table)
