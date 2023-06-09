
from applications.base.models import ParametrosIndicadoresPrevisionales


def get_key_colaborador_data():
    extra_kwargs = {
                    'user_id': 'required',
                    'cargo_id': 'required',
                    'centrocosto_id': 'required',
                    'sucursal_id': 'required',
                    'empresa_id': 'required',
                    'ue_tipotrabajdor': 'required',
                    'ue_tipocontrato': 'required',
                    'ue_fechacontratacion': 'required',
                    'ue_fecharenovacioncontrato': 'required',
                    'ue_horassemanales': 'required',
                    'ue_asignacionfamiliar': 'required',
                    'ue_cargasfamiliares': 'required',
                    'ue_montoasignacionfamiliar': 'required',
                    'ue_sueldobase': 'required',
                    'ue_gratificacion': 'required',
                    'ue_tipogratificacion': 'required',
                    'ue_comiciones': 'required',
                    'ue_porcentajecomicion': 'required',
                    'ue_semanacorrida': 'required',
                }
    keys = extra_kwargs.keys()
    return list(keys)

def get_tope_seguro_cesantia(pip_codigo):
    pip_object = ParametrosIndicadoresPrevisionales.objects.get(pip_codigo=pip_codigo)

    data = {
        "porcentaje_empleador": f"{round(pip_object.pip_rangoini, 1)}%",
        "porcentaje_empleado": f"{round(pip_object.pip_rangofin if not pip_object.pip_rangofin else 0, 1)}%"  
    }

    return data