import streamlit as st

import random

import google.generativeai as genai



try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except:
    st.error("Ключ GEMINI_API_KEY не знайдено в Secrets!")



def get_working_model():

    try:

        # Отримуємо список доступних моделей

        available_models = [m.name for m in genai.list_models()]

        # Пріоритет: 1.5 Flash -> 1.5 Pro -> Pro

        for model_name in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:

            if model_name in available_models:

                return genai.GenerativeModel(model_name)

        for m in genai.list_models():

            if 'generateContent' in m.supported_generation_methods:

                return genai.GenerativeModel(m.name)

    except Exception as e:

        st.error(f"Помилка доступу до моделей: {e}")

    return None


model = get_working_model()

# --- 2. КОНФІГУРАЦІЯ СТОРІНКИ ---
st.set_page_config(
    page_title="SLV", 
    page_icon="💌", 
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-image: url('C:\Users\Sofia\Desktop\пітон\tarot_progect\dIQMZLS.jpg');
    }
    h1 {
        color: #D02090 !important;
        font-family: 'Comic Sans MS', cursive;
        text-align: center;
    }
    .stTextInput label {
        color: #000000 !important;
        font-weight: bold;
    }
    input {
        color: #C71585 !important;
    }
    ::placeholder {
        color: #4B4B4B !important;
    }
    div.stButton > button {
        background-color: #FFC0CB !important;
        color: #5D2E46 !important;
        border: 2px solid #FFB6C1 !important;
        border-radius: 20px !important;
        width: 100% !important;
        font-weight: bold !important;
    }
    .prediction-box {
        background-color: #FFF0F5;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #FFB6C1;
        text-align: center;
        font-size: 20px;
        color: #5D2E46;
        margin-top: 20px; 
        box-shadow: 0px 4px 15px rgba(208, 32, 144, 0.1);
    }
    .card-display {
        background-color: #FFFFFF;
        border: 2px solid #FFB6C1;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        color: #D02090;
        font-weight: bold;
        font-family: 'Comic Sans MS', cursive;
        margin: 5px;
    }
    div[data-testid="stSpinner"] p {
        color: #D02090 !important;
        font-family: 'Comic Sans MS', cursive !important;
        text-align: center !important;
        font-size: 1.1rem;
    }
    div[data-testid="stSpinner"] i {
        color: #D02090 !important;
    </style>
    """, unsafe_allow_html=True)

# --- 4. ЗАГОЛОВОК ТА ВВЕДЕННЯ ---
st.title("Забий на розвиток, деградуй разом з Нами!!!🌸")

question = st.text_input("Давай ніщєта, задавай питання:", placeholder="тут")

# Перевірка на пусте поле
is_disabled = not question.strip()

# --- 5. СПИСОК КАРТ ---
tarot_deck = [
    "Королева Жезлів", "Трійка Мечів", "Сімка Пентаклів", "Блазень", "Десятка Кубків", "Маг", "Вісімка Мечів", "Верховна Жриця", "Лицар Жезлів",
    "Справедливість", "Туз Пентаклів", "Імператриця", "П'ятірка Жезлів", "Місяць", "Дев'ятка Мечів", "Колесо Фортуни", "Король Кубків", "Сімка Жезлів", 
    "Світ", "Паж Мечів", "Двійка Кубків", "Четвірка Пентаклів", "Імператор", "Вісімка Жезлів", "Сонце", "Шістка Мечів", "Помірність", "Трійка Жезлів", "Зірка", 
    "Десятка Мечів", "Ієрофант", "П'ятірка Пентаклів", "Сила", "Туз Жезлів", "Закохані", "Дев'ятка Пентаклів", "Диявол", "Королева Мечів", "Смерть", "Лицар Кубків", 
    "Сімка Мечів", "Четвірка Жезлів", "Відшельник", "Двійка Пентаклів", "Вежа", "Шістка Пентаклів", "Колісниця", "П'ятірка Мечів", "Король Жезлів", "Трійка Кубків", 
    "Суд", "Вісімка Пентаклів", "Повішений", "Десятка Жезлів", "Паж Кубків", "Сімка Кубків", "Королева Пентаклів", "Двійка Мечів", "Туз Кубків", "Шістка Жезлів", 
    "Дев'ятка Жезлів", "Король Мечів", "П'ятірка Кубків", "Лицар Пентаклів", "Трійка Пентаклів", "Четвірка Кубків", "Десятка Пентаклів", "Паж Жезлів", "Вісімка Кубків", 
    "Король Пентаклів", "Двійка Жезлів", "Лицар Мечів", "Шістка Кубків", "Туз Мечів", "Паж Пентаклів", "Четвірка Мечів", "Дев'ятка Кубків", "Королева Кубків"
]

# --- 6. ЛОГІКА РОЗКЛАДУ ---
if st.button("Фух, Амінь", disabled=is_disabled):
    # Випадкові карти
    selected_cards = random.sample(tarot_deck, 3)
    
    # Вивід карт
    cols = st.columns(3)
    for i in range(3):
        cols[i].markdown(f'<div class="card-display">{selected_cards[i]}</div>', unsafe_allow_html=True)
    
    # Запит до Gemini
    if model:
        with st.spinner('Чекай, бо то тобі не квантовий кампутєр...'):
            try:
                prompt = (
                    f"Ти таролог у стилі 'подружки-гадалки', яка може як добре про карти сказати, так і погане, а також давай точну відповідь на запитання. Питання: '{question}'. "
                    f"Випали карти: {', '.join(selected_cards)}. "
                    f"Дай коротке, зухвале, але магічне пророцтво українською мовою. "
                    f"Використовуй емодзі, мати та звертайся до користувача на 'ти'."
                )
                response = model.generate_content(prompt)
                
                # Вивід відповіді у твоєму стилі prediction-box
                st.markdown(f'<div class="prediction-box"><b>Послання Всесвіту:</b><br>{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Помилка ШІ: {e}")
    else:
        st.error("ШІ не підключено")


st.markdown("<br><center style='color: #D02090; font-family: cursive;'>Зроблено з любов'ю!! Ну а також з ненавістю до деяких персон. Саранхе🩷</center>", unsafe_allow_html=True)

