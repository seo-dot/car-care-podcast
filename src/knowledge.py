"""Проверенные факты о Desert Diamond — «источник правды» для экспертного блока.

У car-care.center нет машиночитаемых policies.json/company.json, поэтому сетевые загрузки
отключены: используем зашитые VERIFIED-факты (сняты с сайта вручную). Конкретику по каждой
услуге (что входит, цена, сроки) эксперт берёт со страницы услуги в промпте.
Эксперт и гости опираются ТОЛЬКО на эти факты и не выдумывают цен/сроков/характеристик.
"""

# --- Проверенные факты Desert Diamond (fallback, сеть не нужна) ---
VERIFIED_FALLBACK = {
    "studio_facts": [
        "Desert Diamond is a premium car detailing studio in Dubai (Al Quoz Industrial Area 3, 22nd Street) and Abu Dhabi.",
        "The specialists are European-trained.",
        "Services include: car wrapping, PPF (paint protection film), window tinting, car wash, "
        "polishing, ceramic coating, interior cleaning, scratch repair, rim painting, upholstery, "
        "carbon fiber, body kits, sound deadening, star roof and leather repair.",
        "Light mechanical work is also available: oil change, brake pads, AC and suspension.",
        "Booking is available online at car-care.center.",
    ],
    "price_guide": [
        "Car wash from AED 85.",
        "Detailing packages from around AED 500.",
        "Ceramic coating from AED 300.",
        "Wrapping / PPF up to around AED 6900.",
        "Exact price for a specific service comes only from that service's own page.",
    ],
}


def refresh(force=False):
    """Возвращает проверенные факты Desert Diamond (без сетевых запросов)."""
    return {
        "studio_facts": list(VERIFIED_FALLBACK["studio_facts"]),
        "price_guide": list(VERIFIED_FALLBACK["price_guide"]),
    }


def facts_text(knowledge=None):
    """Компактный блок фактов для промпта."""
    k = knowledge or refresh()
    studio = "\n".join(f"- {x}" for x in k.get("studio_facts", []))
    prices = "\n".join(f"- {x}" for x in k.get("price_guide", []))
    return (
        "VERIFIED DESERT DIAMOND FACTS (use ONLY these for any studio/service/price claims; "
        "never invent prices, durations, materials or guarantees — exact per-service price only "
        "from the service page):\n"
        f"[Studio]\n{studio}\n[Price guide]\n{prices}"
    )


if __name__ == "__main__":
    print(facts_text())
