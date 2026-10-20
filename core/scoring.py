from decimal import Decimal, ROUND_HALF_UP


DIMENSIONS = [
    (1, "I", "I. Disposición al Cambio", [1, 11, 21, 31]),
    (2, "II", "II. Auto-cuestionamiento", [2, 12, 22, 32]),
    (3, "III", "III. Capacidad de Auto-indagación y Espera Reflexiva", [3, 13, 23, 33]),
    (4, "IV", "IV. Riqueza Psíquica y Creatividad", [4, 14, 24, 34]),
    (5, "V", "V. Auto-cuidado para la Autovalidez", [5, 15, 25, 35]),
    (6, "VI", "VI. Posición Anticipada Respecto a la Propia Vejez", [6, 16, 26, 36]),
    (7, "VII", "VII. Posición Anticipada Respecto a la Finitud", [7, 17, 27, 37]),
    (8, "VIII", "VIII. Pérdidas, Vacíos y Compensación con Ganancias", [8, 18, 28, 38]),
    (9, "IX", "IX. Vínculos Intergeneracionales", [9, 19, 29, 39]),
    (10, "X", "X. Diversificación de Vínculos e Intereses", [10, 20, 30, 40]),
]

INVERSE_ITEMS = {
    2,
    4,
    7,
    9,
    12,
    15,
    16,
    18,
    20,
    21,
    23,
    24,
    25,
    30,
    32,
    36,
    38,
    39,
}

OPTION_LABELS = {
    "1": "En desacuerdo",
    "2": "Parcialmente en desacuerdo",
    "3": "Algo de acuerdo",
    "4": "De acuerdo",
}

ITEM_TEXTS = {
    1: "Considero que tengo una personalidad “flexible”",
    2: "Yo soy así y no voy a cambiar",
    3: "Suelo hacer, cada tanto, un balance de mi vida",
    4: "Rechazaría participar en juegos en los que haya que utilizar la imaginación",
    5: "Cuando me dan indicaciones de cómo cuidar mi salud, las llevo a la práctica",
    6: "Es bueno darse cuenta que uno va envejeciendo",
    7: "Cuando uno es viejo sólo le queda esperar la muerte",
    8: "A pesar de las pérdidas (materiales, afectivas) busco el modo de seguir adelante",
    9: "Nadie considera ni respeta a las personas mayores",
    10: "Trato de mantenerme al tanto de lo que pasa a mi alrededor",
    11: "Puedo adaptarme a los cambios",
    12: "Tener humildad es contraproducente",
    13: "Busco darle sentido propio a mi vida, no el que desean otras personas para mí",
    14: "Soy una persona con buen humor",
    15: "Cuando siento en mi cuerpo un límite siempre me sobreexijo",
    16: "En la vejez ya es tarde para aprender algo nuevo",
    17: "Tengo en cuenta que algunas circunstancias podrían impedirme cumplir con algunas de las metas que me propuse en la vida",
    18: "Al dejar de trabajar la vida se derrumba",
    19: "Disfruto de estar con gente más joven y más vieja",
    20: "En la vida hay que concentrarse en un único objetivo",
    21: "Me cuesta modificar mi punto de vista",
    22: "Acepto que la vida no gire a mi alrededor",
    23: "Me considero una persona impulsiva",
    24: "Con la vejez se acaban las fantasías y el deseo sexual",
    25: "Cuando se llega a viejo los demás deciden por uno",
    26: "En la vejez se está a tiempo para encarar nuevos proyectos",
    27: "Me reconforta pensar que, luego de que muera, algo de mí quedará en quienes me conocieron",
    28: "Me gratifica relatar recuerdos de lo que viví",
    29: "De diversas maneras, las personas mayores pueden aportarle mucho a los más jóvenes",
    30: "Siento que, ante la ausencia de alguien significativo, mi vida carecería de sentido",
    31: "Voy ajustando mis metas a mis posibilidades",
    32: "Me molesta reconocer que me equivoco",
    33: "Le doy importancia a conectarme con mi vida interior",
    34: "Puedo fantasear con lo que anhelo",
    35: "Si tuviera que usar bastón o audífonos, lo aceptaría",
    36: "Me molestaría tener que hacer todo más despacio",
    37: "Puedo soportar la idea de que la vida tiene un fin",
    38: "Trato de evitar tener tiempo libre porque no sabría en qué ocuparlo",
    39: "Para las personas mayores lo mejor es estar con gente de su edad.",
    40: "¿Cuál o cuáles de estos aspectos ocupan un lugar de relevancia en su vida actual?",
}

RESULTADOS_HEADERS = (
    ["ID"]
    + [label for _, _, label, _ in DIMENSIONS]
    + [
        "PUNTAJE TOTAL (0–120)",
        "Nivel del total",
        "N° de dimensiones en déficit",
        "Áreas de vulnerabilidad (dimensiones en nivel Bajo)",
    ]
    + [f"Dimensión {roman}" for _, roman, _, _ in DIMENSIONS]
)


def item_score(item_number: int, raw_value):
    """
    Convert raw answer to corrected item score.

    Items 1-39:
        Direct: option - 1
        Inverse: 4 - option

    Item 40:
        Count of selected aspects: 0 for none, 1, 2, or 3 for three or more.
    """
    if raw_value is None:
        return None

    try:
        raw_value = int(raw_value)
    except (TypeError, ValueError):
        return None

    if item_number == 40:
        return min(max(raw_value, 0), 3)

    if raw_value < 1 or raw_value > 4:
        return None

    if item_number in INVERSE_ITEMS:
        return 4 - raw_value

    return raw_value - 1


def dimension_score(item_numbers, answers: dict):
    """
    Calculate one dimension score.

    answers:
        {item_number: raw_value}

    Rules:
        - If more than one item is missing, return None.
        - If exactly one item is missing, prorate:
              round(sum_present * 4 / 3)
    """
    scores = []

    for item_number in item_numbers:
        raw_value = answers.get(item_number)
        scores.append(item_score(item_number, raw_value))

    present_scores = [score for score in scores if score is not None]
    missing_count = len(scores) - len(present_scores)

    if missing_count > 1:
        return None

    if missing_count == 1:
        value = Decimal(sum(present_scores)) * Decimal(4) / Decimal(3)
        return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    return sum(present_scores)


def dimension_level(score):
    if score is None:
        return None

    if score <= 4:
        return "Baja"

    if score <= 8:
        return "Moderada"

    return "Alta"


def total_level(score):
    if score is None:
        return None

    if score <= 40:
        return "Baja presencia de factores protectores"

    if score <= 89:
        return "Moderada presencia de factores protectores"

    return "Alta presencia de factores protectores"


def compute_results(answers: dict):
    """
    Compute all FAPPREN VA results.

    Returns a dictionary with:
        - dimensions: list for templates
        - dimension_scores: {dimension_number: score}
        - dimension_levels: {dimension_number: level}
        - total
        - total_level
        - deficits_count
        - areas
    """
    dimension_rows = []
    dimension_scores = {}
    dimension_levels = {}
    vulnerable_dimensions = []

    for number, roman, label, item_numbers in DIMENSIONS:
        score = dimension_score(item_numbers, answers)
        level = dimension_level(score)

        dimension_scores[number] = score
        dimension_levels[number] = level

        dimension_rows.append(
            {
                "number": number,
                "roman": roman,
                "label": label,
                "score": score,
                "level": level or "",
            }
        )

        if score is not None and score <= 4:
            vulnerable_dimensions.append(roman)

    if all(score is not None for score in dimension_scores.values()):
        total = sum(score for score in dimension_scores.values() if score is not None)
    else:
        total = None

    level_total = total_level(total)
    areas = "Sin alertas" if not vulnerable_dimensions else "; ".join(vulnerable_dimensions)

    return {
        "dimensions": dimension_rows,
        "dimension_scores": dimension_scores,
        "dimension_levels": dimension_levels,
        "total": total,
        "total_level": level_total,
        "deficits_count": len(vulnerable_dimensions),
        "areas": areas,
    }