import datetime

from py_arg_reports.reporters.libro_sueldo_digital.tools import INDICE_TIPO_LIQUIDACIONES


def process_reg1(cuit: str, periodo: datetime.date, q_empleados: int, nro_liq: int, tipo_liq: str, dias_base: int = None) -> tuple:
    """ Generacion txt de Libro Sueldos Digital
        Registro 1 Datos referenciales del envío de la liquidacion
        Args:
            cuit: str, CUIT del empleador
            periodo: datetime.date, fecha de la liquidacion
            q_empleados: int, cantidad de empleados liquidados
            nro_liq: int, numero de liquidacion
            tipo_liq: str, tipo de liquidacion ('M'=mes; 'Q'=quincena; 'S'=semanal)
            dias_base: int, opcional, días base de la liquidación (15 para quincena, 30 para mes)
        Retorna:
            (Resultado, Error, Registro1)
            - True, None, str: si todo salió bien
            - False, str, None: si falla
    """

    # Período en formato AAAAMM
    periodo_str = periodo.strftime('%Y%m')
    tipo_liq_aceptadas = INDICE_TIPO_LIQUIDACIONES.keys()

    # Validaciones
    cuit = cuit.replace('-', '')
    if len(cuit) != 11:
        return False, 'CUIT incorrecto', None

    if q_empleados < 1:
        return False, 'Cantidad de empleados incorrecta', None

    if nro_liq < 1:
        return False, 'Numero de liquidacion incorrecto', None

    if tipo_liq not in tipo_liq_aceptadas:
        return False, 'Tipo de liquidacion no aceptada', None

    tipo_liquidacion = INDICE_TIPO_LIQUIDACIONES[tipo_liq]

    # Pendiente tipo de liquidacion rectificativa
    resp = f'01{cuit}SJ'
    resp += periodo_str
    resp += tipo_liquidacion
    resp += str(nro_liq).zfill(5)

    if dias_base is not None:
        ds_base = int(dias_base)
    elif tipo_liquidacion == 'Q':
        ds_base = 15
    elif tipo_liquidacion == 'S':
        ds_base = 7
    else:
        ds_base = 30

    resp += str(ds_base).zfill(2) + str(q_empleados).zfill(6)

    return True, None, resp

