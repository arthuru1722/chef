import copy

from data.defaults import DEFAULT_VALUES, normalize_old_keys
from data.fields import FIELD_GROUPS


def empty_values():
    return normalize_old_keys(copy.deepcopy(DEFAULT_VALUES))


def values_from_form(form):
    values = empty_values()
    for _, fields in FIELD_GROUPS:
        for key, _ in fields:
            values[key] = form.get(key, "").strip()

    values["autorizaImagem"] = form.get("autorizaImagem") == "on"
    values["antecedenciaCredito"] = form.get("antecedenciaCredito", values["antecedenciaCredito"]).strip()
    values["antecedenciaDesistencia"] = form.get(
        "antecedenciaDesistencia", values["antecedenciaDesistencia"]
    ).strip()

    materials = []
    material_count = max(3, int(form.get("material_count", "3") or 3))
    for index in range(material_count):
        nome = form.get(f"material_nome_{index}", "").strip()
        custo = form.get(f"material_custo_{index}", "").strip()
        if nome or custo or index < 3:
            materials.append({"nome": nome, "custo": custo})
    values["materiais"] = materials
    return values
