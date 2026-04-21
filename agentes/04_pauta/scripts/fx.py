"""
fx.py — Tipo de cambio CCL en tiempo real para conversion de presupuestos ARS -> USD.

Fuente: argentinadatos.com (API publica, sin auth).
"""

import requests


def get_ccl() -> float:
    """
    Devuelve el tipo de cambio CCL actual (precio de venta, ARS por USD).

    Returns:
        float: precio de venta del CCL.

    Raises:
        RuntimeError: si no puede obtener la cotizacion.
    """
    try:
        r = requests.get(
            "https://api.argentinadatos.com/v1/cotizaciones/dolares",
            timeout=10,
        )
        data = r.json()
        ccl_records = [d for d in data if d.get("casa") == "contadoconliqui"]
        if ccl_records:
            ultimo = sorted(ccl_records, key=lambda x: x["fecha"])[-1]
            return float(ultimo["venta"])
    except Exception:
        pass

    raise RuntimeError(
        "No se pudo obtener el CCL automaticamente. "
        "Ingresalo manualmente: ars_a_usd_centavos(monto, ccl=VALOR)."
    )


def ars_a_usd_centavos(ars: float, ccl: float | None = None) -> int:
    """
    Convierte un monto en ARS a centavos USD usando el CCL.

    Args:
        ars: monto en pesos argentinos.
        ccl: tipo de cambio CCL. Si es None, lo busca automaticamente.

    Returns:
        int: centavos USD (lo que Meta espera en daily_budget).
    """
    if ccl is None:
        ccl = get_ccl()
    return round((ars / ccl) * 100)


if __name__ == "__main__":
    ccl = get_ccl()
    print(f"CCL actual: ${ccl:,.2f} ARS/USD")
    ejemplo = 14286
    centavos = ars_a_usd_centavos(ejemplo, ccl)
    print(f"{ejemplo} ARS/dia = {centavos} centavos USD (~USD {centavos/100:.2f})")
