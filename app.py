
import base64
import random
import html
import google.generativeai as genai
import streamlit as st


# --- 1. КОНФІГУРАЦІЯ СТОРІНКИ ---
st.set_page_config(
    page_title="SLV",
    page_icon="💌",
    layout="centered"
)


# --- 2. ПІДКЛЮЧЕННЯ GEMINI ---
model = None

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)

    def get_working_model():
        try:
            available_models = list(genai.list_models())

            preferred_models = [
                "models/gemini-1.5-flash",
                "models/gemini-1.5-pro",
                "models/gemini-pro",
            ]

            available_names = [m.name for m in available_models]

            for model_name in preferred_models:
                if model_name in available_names:
                    return genai.GenerativeModel(model_name)

            for m in available_models:
                if "generateContent" in m.supported_generation_methods:
                    return genai.GenerativeModel(m.name)

        except Exception as e:
            st.error(f"Помилка доступу до моделей: {e}")

        return None

    model = get_working_model()

except Exception:
    st.error("Ключ GEMINI_API_KEY не знайдено в Secrets!")


# --- 3. ФОН І СТИЛІ ---
def set_bg_local(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/avif;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}

            h1 {{
                color: #FFC0CB !important;
                font-family: 'Comic Sans MS', cursive;
                text-align: center;
                text-shadow: 1px 1px 2px black;
            }}

            .stTextInput label {{
                color: #000000 !important;
                font-weight: bold;
            }}

            input {{
                color: #C71585 !important;
            }}

            input::placeholder {{
                color: #4B4B4B !important;
            }}

            div.stButton > button {{
                background-color: #FFC0CB !important;
                color: #5D2E46 !important;
                border: 2px solid #F19CBB !important;
                border-radius: 20px !important;
                width: 100% !important;
                font-weight: bold !important;
            }}

            div.stButton > button:hover {{
                background-color: #FFB6C1 !important;
                border-color: #F19CBB !important;
            }}

            .prediction-box {{
                background-color: #FFF0F5;
                padding: 20px;
                border-radius: 15px;
                border: 2px solid #FFB6C1;
                text-align: center;
                font-size: 20px;
                color: #5D2E46;
                margin-top: 20px;
                margin-bottom: 60px;
                box-shadow: 0px 4px 15px rgba(208, 32, 144, 0.1);
            }}

            .card-display {{
                background-color: #FFFFFF;
                border: 2px solid #FFB6C1;
                padding: 15px;
                border-radius: 15px;
                text-align: center;
                color: #D02090;
                font-weight: bold;
                font-family: 'Comic Sans MS', cursive;
                margin: 5px;
            }}

            div[data-testid="stSpinner"] p {{
                color: #D02090 !important;
                font-family: 'Comic Sans MS', cursive !important;
                text-align: center !important;
                font-size: 1.1rem;
            }}

            div[data-testid="stSpinner"] i {{
                color: #D02090 !important;
            }}

            .footer-klitschko {{
                position: fixed;
                bottom: 10px;
                left: 0;
                width: 100%;
                text-align: center;
                color: #FFC0CB;
                font-family: 'Comic Sans MS', cursive;
                font-size: 24px;
                font-weight: bold;
                z-index: 999999;
                pointer-events: none;
                text-shadow: 1px 1px 2px black;
            }}

            @media (max-width: 600px) {{
                .footer-klitschko {{
                    font-size: 18px;
                    bottom: 8px;
                }}
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    except FileNotFoundError:
        st.warning(
            "Фонове зображення не знайдено. "
            "Перевір назву та розташування AVIF-файлу."
        )

    except Exception as e:
        st.error(f"Не вдалося завантажити фон: {e}")


set_bg_local(
    "abstract-pink-pastel-shadow-light-diagonal-shape-background_164305-3819.avif"
)


# --- 4. ЗАГОЛОВОК І ПИТАННЯ ---
st.title("Наша абревіатура СЛВ - Сука, Любить Він мене?")

question = st.text_input(
    "Давай ніщєта, задавай питання:",
    placeholder="тут"
)

is_disabled = not question.strip()


# --- 5. КОЛОДА ТАРО ---
tarot_deck = [
    "Королева Жезлів",
    "Трійка Мечів",
    "Сімка Пентаклів",
    "Блазень",
    "Десятка Кубків",
    "Маг",
    "Вісімка Мечів",
    "Верховна Жриця",
    "Лицар Жезлів",
    "Справедливість",
    "Туз Пентаклів",
    "Імператриця",
    "П'ятірка Жезлів",
    "Місяць",
    "Дев'ятка Мечів",
    "Колесо Фортуни",
    "Король Кубків",
    "Сімка Жезлів",
    "Світ",
    "Паж Мечів",
    "Двійка Кубків",
    "Четвірка Пентаклів",
    "Імператор",
    "Вісімка Жезлів",
    "Сонце",
    "Шістка Мечів",
    "Помірність",
    "Трійка Жезлів",
    "Зірка",
    "Десятка Мечів",
    "Ієрофант",
    "П'ятірка Пентаклів",
    "Сила",
    "Туз Жезлів",
    "Закохані",
    "Дев'ятка Пентаклів",
    "Диявол",
    "Королева Мечів",
    "Смерть",
    "Лицар Кубків",
    "Сімка Мечів",
    "Четвірка Жезлів",
    "Відшельник",
    "Двійка Пентаклів",
    "Вежа",
    "Шістка Пентаклів",
    "Колісниця",
    "П'ятірка Мечів",
    "Король Жезлів",
    "Трійка Кубків",
    "Суд",
    "Вісімка Пентаклів",
    "Повішений",
    "Десятка Жезлів",
    "Паж Кубків",
    "Сімка Кубків",
    "Королева Пентаклів",
    "Двійка Мечів",
    "Туз Кубків",
    "Шістка Жезлів",
    "Дев'ятка Жезлів",
    "Король Мечів",
    "П'ятірка Кубків",
    "Лицар Пентаклів",
    "Трійка Пентаклів",
    "Четвірка Кубків",
    "Десятка Пентаклів",
    "Паж Жезлів",
    "Вісімка Кубків",
    "Король Пентаклів",
    "Двійка Жезлів",
    "Лицар Мечів",
    "Шістка Кубків",
    "Туз Мечів",
    "Паж Пентаклів",
    "Четвірка Мечів",
    "Дев'ятка Кубків",
    "Королева Кубків",
]


# --- 6. РОЗКЛАД ТАРО ---
if st.button("Летс гоу бічессссс", disabled=is_disabled):

    selected_cards = random.sample(tarot_deck, 3)

    cols = st.columns(3)

    for i in range(3):
        cols[i].markdown(
            f'<div class="card-display">{selected_cards[i]}</div>',
            unsafe_allow_html=True,
        )

    if model:
        with st.spinner("Ну їбать"):
            try:
                prompt = (
                    f"Ти таролог у стилі 'подружки-гадалки', яка може як добре про карти сказати, так і погане, а також давай точну відповідь на запитання. Питання: '{question}'. "
                    f"Випали карти: {', '.join(selected_cards)}. "
                    f"Дай коротке, зухвале, але магічне пророцтво українською мовою. В кінці можеш зробити висновок того всього. "
                    f"Використовуй емодзі, мати та звертайся до користувача на 'ти'."
                )

                response = model.generate_content(prompt)

                # Безпечне відображення відповіді ШІ
                answer = html.escape(response.text).replace(
                    "\n", "<br>"
                )

                st.markdown(
                    f"""
                    <div class="prediction-box">
                        <b>Послання Всесвіту:</b>
                        <br><br>
                        {answer}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"Помилка ШІ: {e}")

    else:
        st.error(
            "ШІ не підключено. Перевір GEMINI_API_KEY "
            "у Secrets та доступність моделі Gemini."
        )


# --- 7. НАПИС УНИЗУ ЕКРАНА ---
st.markdown(
    """
    <div class="footer-klitschko">
        КЛІЧКОООООООО
    </div>
    """,
    unsafe_allow_html=True,
)
