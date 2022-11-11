from datetime import date, datetime, timedelta


def get_cur_datetime() -> dict:
    cur = {}
    fecha_hoy = datetime.now() + timedelta(days=1)
    hora = fecha_hoy - (fecha_hoy - datetime.min) % timedelta(minutes=30)
    fecha_fin = fecha_hoy + timedelta(days=90)

    cur['now'] = datetime.now().strftime("%Y-%m-%d")
    cur['fecha_actual'] = fecha_hoy.strftime("%Y-%m-%d")
    cur['fecha_fin'] = fecha_fin.strftime("%Y-%m-%d")
    cur['hora'] = hora.strftime("%H:%M")

    return cur


if __name__ == '__main__':
    print(get_cur_datetime())
