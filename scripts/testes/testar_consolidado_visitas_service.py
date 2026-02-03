import pandas as pd

from scripts.servicos.consolidado_visitas_service import (
    consolidar_visitas_mensal_por_tecnico
)


def test_consolidar_visitas_mensal_por_tecnico():
    """
    Deve consolidar corretamente o total de visitas por técnico
    em um mês e ano específicos.
    """

    # Arrange
    df_visitas = pd.DataFrame([
        {"tecnico": "João", "ano": 2025, "mes": 1},
        {"tecnico": "João", "ano": 2025, "mes": 1},
        {"tecnico": "Maria", "ano": 2025, "mes": 1},
        {"tecnico": "Maria", "ano": 2025, "mes": 2},
        {"tecnico": "Pedro", "ano": 2024, "mes": 1},
    ])

    # Act
    resultado = consolidar_visitas_mensal_por_tecnico(
        df_visitas=df_visitas,
        mes=1,
        ano=2025
    )

    # Assert
    esperado = pd.DataFrame([
        {"tecnico": "João", "total_visitas": 2},
        {"tecnico": "Maria", "total_visitas": 1},
    ])

    pd.testing.assert_frame_equal(resultado, esperado)
