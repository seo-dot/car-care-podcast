"""Формат шоу «Car Detailing Podcast» (Desert Diamond) и вся промпт-логика.

Каждый выпуск — эпизод-ОТЗЫВ об опыте КОНКРЕТНОЙ услуги детейлинга: ведущие + гость
(рассказывает, как записался, как прошла процедура, результат, сервис) + короткий блок
эксперта Desert Diamond с полезным советом по уходу (строго по фактам). Чтобы выпуски
были РАЗНЫМИ, приложение чередует историю гостя, самого гостя, тему эксперта и рубрику.

Честность (важно и для доверия, и для YouTube):
  - Гость — ИЛЛЮСТРАТИВНЫЙ персонаж бренда, а не выдаваемый за реального проверенного
    клиента. Впечатления — живые и позитивные, но без выдуманных «пруфов»/звёздных рейтингов.
  - Эксперт говорит ТОЛЬКО факты из knowledge.py + конкретику со страницы услуги.
    Никаких выдуманных цен/сроков/характеристик.
  - Не называем шоу «прямым эфиром» — подкаст предзаписан.
"""

HOST_A = "Alex"            # ведущий (муж.)
HOST_B = "Sam"             # ведущая (жен.)
EXPERT = "Omar"            # эксперт Desert Diamond (советы по уходу)

SHOW_NAME = "Car Detailing Podcast"

# --- Базовые правила шоу (в каждом выпуске) ---
BASE_RULES = f"""You write ONE episode of the audio podcast "{SHOW_NAME}" by Desert Diamond
(car-care.center) — a premium car detailing studio in Dubai (Al Quoz Industrial Area 3) and
Abu Dhabi. Audio only. English. Aim for 1000-1400 words — a full, immersive episode, not a teaser.

Recurring cast:
- {HOST_A}: male host, warm and energetic, keeps the show moving.
- {HOST_B}: female host, sharp and curious, asks the good questions.
- {EXPERT}: Desert Diamond's detailing expert. Appears for a short expert segment with ONE
  genuinely useful care tip about TODAY'S service. He NEVER invents prices, durations, materials
  or guarantees. PRICE RULE: he may state a price ONLY if the input 'Price (AED)' field (taken
  from this service's own page) has one. The studio-wide price examples in the FACTS block are
  general background ONLY — never quote them as this service's price (e.g. do NOT say
  "ceramic from AED 300" in a dent-repair episode). If this service has no price, don't mention
  numbers — say it depends on the car and the specific service.

Episode flow (keep this order, keep it natural, not robotic):
1) Cold open + hosts introduce today's SERVICE and welcome the guest.
2) GUEST STORY (the heart of the episode — make it the LONGEST part, 500+ words):
   the guest talks in DETAIL, like a real person on a podcast, not an ad, about getting THIS
   detailing service done at Desert Diamond. Cover, concretely:
   - why they wanted it and how they booked (online / call), how easy scheduling was;
   - arriving at the Al Quoz (or Abu Dhabi) studio: how it looked, how clean and professional;
   - the PROCESS step by step and roughly how long it took;
   - the RESULT — how the car looked/felt afterwards, before-and-after impressions;
   - the SERVICE — how the specialists explained things, care and attention to detail;
   - genuine emotion — whether it was worth it and how they felt driving away.
   The hosts react, ask follow-up questions, keep it a real back-and-forth conversation.
3) EXPERT SEGMENT with {EXPERT}: a short, genuinely useful car-care tip, using ONLY the FACTS
   and the service page details.
4) SEGMENT: the short recurring rubric given in the input.
5) (If GIVEAWAY is enabled) the giveaway announcement with its real mechanics.
6) Warm outro + one soft booking nudge to car-care.center (Dubai and Abu Dhabi).

Style — make it sound like a REAL conversation, not a script being read:
- Short lines: mostly 1-2 sentences, sometimes just a few words ("Wait, really?", "No way.", "Right?").
- Natural and chatty: contractions, little reactions ("honestly", "ngl", "oh that's nice"), the
  hosts jumping in, light friendly interruptions and overlaps, finishing each other's thoughts.
- The guest talks like a real person recalling it — not reading a paragraph. Break their story
  into many small back-and-forth turns with the hosts reacting and asking follow-ups.
- Keep concrete specifics (the studio, the process, the finish), but spread across the chat.
- Still stay honest (see rules below).

Honesty rules (strict):
- The guest is an ILLUSTRATIVE brand character, NOT presented as a verified named customer
  review. Keep it authentic and positive but never fabricate specific proof, star ratings or
  claims like "verified customer".
- Never invent durations, materials, warranties or results.
- PRICES: quote a price ONLY if the input 'Price (AED)' field for THIS service has one, and tie
  it to this service. Never present the general studio price examples from FACTS as this
  service's price, and never label any number as "verified".
- Never call the show or the giveaway "live" / "in real time" — it is pre-recorded.
- One booking nudge total. No fake urgency, no bashing other studios.

Return STRICT JSON only (no markdown fences), shape:
{{
  "youtube_title": "ENGLISH review headline, <=100 chars, EXACTLY: 'Review of {{Service}} at Desert Diamond {{City}}' (if city unknown: 'Review of {{Service}} at Desert Diamond'). {{Service}} = the input 'Service (clean name)' field, {{City}} = the input 'City' field. Show's experience format — NOT a verified review by a specific real named customer.",
  "episode_title": "short episode title with the service name",
  "episode_description": "EXACTLY this one line: 'Car Detailing Podcast: a guest's experience with {{Service}} at Desert Diamond in {{City}}: {{service_url}}' where {{service_url}} is the full 'Service page' URL. No price, no extra sentences — the link must stay visible.",
  "lines": [{{"speaker": "A|B|G|E", "text": "..."}}]
}}
Speakers: A={HOST_A}, B={HOST_B}, G=guest, E={EXPERT} (expert). Alternate naturally and often;
keep most lines to 1-2 short sentences (some just a few words). Prefer MANY short turns over few long ones."""


# --- Истории подачи гостя (флейвор рассказа) ---
STORY_ANGLES = [
    {"key": "daily-driver", "name": "Daily driver refresh",
     "prompt": "Guest story flavor: an everyday car owner finally treating their daily driver to "
               "this service and being surprised by the difference."},
    {"key": "new-car", "name": "New car protection",
     "prompt": "Guest story flavor: someone who just bought a car and wanted to protect it from "
               "day one with this service."},
    {"key": "before-sale", "name": "Before selling",
     "prompt": "Guest story flavor: a guest prepping their car to look its best before selling or "
               "handing it back, and how this service helped."},
    {"key": "special-occasion", "name": "Special occasion",
     "prompt": "Guest story flavor: getting the car ready for a special moment (wedding, trip, "
               "photoshoot) and wanting it flawless."},
    {"key": "summer-heat", "name": "UAE heat & sand",
     "prompt": "Guest story flavor: dealing with Dubai heat, sun and desert dust, and how this "
               "service protects or restores the car."},
    {"key": "fix-damage", "name": "Fixing wear",
     "prompt": "Guest story flavor: a guest bothered by swirl marks, scratches, stains or dull "
               "paint who finally got it sorted with this service."},
    {"key": "enthusiast", "name": "Car enthusiast",
     "prompt": "Guest story flavor: a detail-obsessed car enthusiast who is picky and was won "
               "over by the quality of the work."},
]

# --- Гости (ротация: разные нации, соло/пары). Персона — иллюстративная. ---
GUESTS = [
    {"key": "uk-solo", "seed": "a British expat in Dubai, dry humour"},
    {"key": "german-couple", "seed": "a German couple, precise and detail-loving"},
    {"key": "indian-pro", "seed": "an Indian professional, warm and expressive"},
    {"key": "saudi-local", "seed": "a Saudi visitor who knows cars, relaxed and proud"},
    {"key": "american-creator", "seed": "an American content creator, upbeat and visual"},
    {"key": "french-couple", "seed": "a French couple, stylish and particular"},
    {"key": "russian-expat", "seed": "a Russian-speaking expat living in Dubai, cool and candid"},
    {"key": "nigerian-solo", "seed": "a Nigerian entrepreneur, curious and joyful"},
    {"key": "chinese-couple", "seed": "a Chinese couple, elegant and detail-loving"},
    {"key": "emirati-local", "seed": "an Emirati local car enthusiast, generous host energy"},
]

# --- Темы экспертного блока (Omar) — каждая опирается на FACTS/страницу услуги ---
EXPERT_TOPICS = [
    {"key": "ceramic-vs-wax", "q": "What's the real difference between ceramic coating and wax?"},
    {"key": "ppf", "q": "When is paint protection film (PPF) worth it?"},
    {"key": "wash-frequency", "q": "How often should I wash my car in the UAE climate?"},
    {"key": "interior-care", "q": "How do I keep the interior and leather in good shape?"},
    {"key": "tint-benefits", "q": "What does quality window tinting actually do for me here?"},
    {"key": "swirl-marks", "q": "What causes swirl marks and how do you remove them?"},
    {"key": "maintain-coating", "q": "How do I maintain a ceramic coating after it's applied?"},
    {"key": "sun-heat", "q": "How do I protect paint and interior from Dubai sun and heat?"},
]

# --- Рубрики (короткий повторяющийся блок) ---
SEGMENTS = [
    {"key": "care-lifehack", "name": "Car-care life-hack",
     "prompt": "Short rubric 'Car-care life-hack': one genuinely useful, FACTS-consistent "
               "detailing/maintenance tip for UAE drivers."},
    {"key": "before-after", "name": "Before & after",
     "prompt": "Short rubric 'Before & after': hosts describe the kind of transformation this "
               "service typically delivers (honestly, no exaggerated claims)."},
    {"key": "myth-busting", "name": "Myth busting",
     "prompt": "Short rubric 'Myth busting': hosts bust one common car-detailing myth, staying "
               "consistent with the FACTS."},
    {"key": "service-duel", "name": "Service duel",
     "prompt": "Short rubric 'Service duel': hosts playfully compare which situation today's "
               "service is the best fit for."},
]

# --- Розыгрыш (реальная механика; НЕ «прямой эфир») ---
GIVEAWAY = {
    "every_n_episodes": 3,   # анонс каждые N выпусков
    "prize": "a free premium car wash at Desert Diamond",
    "how_to_enter": "subscribe to the channel and leave a comment with your car",
    "prompt": (
        "GIVEAWAY block: announce an ongoing Desert Diamond giveaway. Prize: {prize}. To enter: {how}. "
        "State clearly it's easy and free to enter and the winner is announced in a future episode "
        "and on Desert Diamond's social channels. Do NOT say 'live' or 'right now on air'. Keep it short."
    ),
}


def plan_episode(index):
    """Детерминированно собирает состав выпуска по его номеру — соседние выпуски разные."""
    story = STORY_ANGLES[index % len(STORY_ANGLES)]
    guest = GUESTS[index % len(GUESTS)]
    topic = EXPERT_TOPICS[index % len(EXPERT_TOPICS)]
    segment = SEGMENTS[index % len(SEGMENTS)]
    giveaway = (index % GIVEAWAY["every_n_episodes"]) == 0
    return {
        "index": index,
        "story": story,
        "guest": guest,
        "expert_topic": topic,
        "segment": segment,
        "giveaway": giveaway,
    }


def build_system_prompt(plan):
    parts = [BASE_RULES, "", "This episode's setup:",
             f"- {plan['story']['prompt']}",
             f"- Guest persona (illustrative): {plan['guest']['seed']}.",
             f"- Expert question for {EXPERT}: \"{plan['expert_topic']['q']}\" (answer ONLY from FACTS).",
             f"- {plan['segment']['prompt']}"]
    if plan["giveaway"]:
        parts.append("- " + GIVEAWAY["prompt"].format(prize=GIVEAWAY["prize"], how=GIVEAWAY["how_to_enter"]))
    else:
        parts.append("- No giveaway this episode.")
    return "\n".join(parts)
