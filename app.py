# app.py  — wersja z oddzielonymi sekcjami i nową logiką formularza
import streamlit as st
from io import StringIO

st.set_page_config(page_title="Brief Generator", layout="centered")

# --- mały CSS dla ramek sekcji ---
st.markdown(
    """
    <style>
    .section {border:1px solid #d0d0d0; padding:1.2rem; border-radius:6px;
              margin-bottom:1.5rem; background:#fafafa;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Generator promptów do briefów graficznych")

# --- 1. FORMULARZ -------------------------------------------------------------
st.header("1. Wypełnij formularz")

# 1A. TYP MATERIAŁU
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("Typ materiałów i format")
    material_parent = st.radio(
        "Wybierz kategorię:",
        ["Grafiki reklamowe", "Materiały drukowane"],
    )

    if material_parent == "Grafiki reklamowe":
        channel = st.radio(
            "Kanał:",
            ["Facebook", "Google Ads", "Mail", "Strona www", "Inne"],
        )
        if channel == "Inne":
            channel = st.text_input("Podaj kanał / format")
        page_count = None
        sub_format = None

    else:  # Materiały drukowane
        channel = st.radio(
            "Format drukowany:",
            ["Ulotki", "Reklama prasowa", "Rollup", "Inne"],
        )

        if channel == "Ulotki":
            page_count = st.number_input(
                "Ilość stron ulotki", min_value=1, value=2
            )
            sub_format = st.text_input(
                "Format ulotki (np. A5, DL, custom)"
            )
        elif channel == "Reklama prasowa":
            sub_format = st.radio(
                "Format reklamy:",
                [
                    "1 strona",
                    "½ strony pionowo",
                    "½ strony poziomo",
                    "Inny",
                ],
            )
            if sub_format == "Inny":
                sub_format = st.text_input("Podaj format")
            page_count = None
        elif channel == "Rollup":
            sub_format = st.radio("Format roll-upa:", ["85x200", "100x200"])
            page_count = None
        else:  # Inne
            sub_format = st.text_input("Podaj format")
            page_count = None
    st.markdown("</div>", unsafe_allow_html=True)

# 1B. CEL + CTA
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("Cel i CTA")

    goal_parent = st.radio("Cel:", ["Sprzedaż", "Leadowanie", "Inne"])

    # Szczegóły celu
    if goal_parent == "Sprzedaż":
        goal_detail = st.radio(
            "Konkretne zadanie:",
            [
                "Zachęcenie do zakupu",
                "Prezentacja produktu",
                "Promocja",
            ],
        )
    elif goal_parent == "Leadowanie":
        goal_detail = st.radio(
            "Konkretne zadanie:",
            [
                "Pobranie materiału (ebook, PDF, raport)",
                "Zapis na webinar / wydarzenie",
            ],
        )
    else:
        goal_detail = st.text_input("Opisz cel")

    # Dodatkowe treści zależnie od wybranego szczegółu
    promotion_text = offer_text = lead_magnet = ""
    if goal_detail == "Promocja":
        promotion_text = st.text_input("Treść promocji (krótko)")
    if goal_detail in ["Zachęcenie do zakupu", "Prezentacja produktu"]:
        offer_text = st.text_area("Opis oferty / produktu")
    if goal_parent == "Leadowanie":
        lead_magnet = st.text_area("Opis lead magnetu")

    # CTA – zestaw zależny od celu
    if goal_parent == "Sprzedaż":
        cta = st.radio(
            "CTA:",
            ["Kup teraz", "Zamów dziś", "Skorzystaj z promocji", "Odbierz zniżkę", "Inne"],
        )
    elif goal_parent == "Leadowanie":
        cta = st.radio(
            "CTA:",
            ["Zapisz się", "Dołącz do nas", "Pobierz za darmo", "Odbierz materiał", "Inne"],
        )
    else:
        cta = st.text_input("CTA (wpisz dowolne)")

    if cta == "Inne":
        cta = st.text_input("Podaj własne CTA")

    st.markdown("</div>", unsafe_allow_html=True)

# 1C. INFORMACJE KREATYWNE
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("Grupa docelowa, stylistyka, elementy")

    target_audience = st.text_area("Grupa docelowa")
    # Kolorystyka
    color_choice = st.radio(
        "Kolorystyka:",
        ["zgodna z key visualem produktu / marki", "inna"],
    )
    colorscheme = (
        color_choice
        if color_choice.startswith("zgodna")
        else st.text_input("Opisz kolorystykę")
    )

    # Elementy obowiązkowe
    req = st.multiselect(
        "Niezbędne elementy:",
        ["logo", "informacja o promocji"],
    )
    req_extra = st.text_input("Inne elementy (opcjonalnie)")
    if req_extra:
        req.append(req_extra)
    required_elements = ", ".join(req) if req else "brak"

    # Styl
    style_sel = st.radio(
        "Styl graficzny:",
        [
            "Minimalistyczny",
            "Profesjonalny",
            "Nowoczesny",
            "Futurystyczny",
            "Technologiczny",
            "Emocjonalny",
            "Luksusowy",
            "Casualowy – lekki",
            "Inny",
        ],
    )
    style = (
        st.text_input("Opisz styl") if style_sel == "Inny" else style_sel
    )

    st.markdown("</div>", unsafe_allow_html=True)

# 1D. PRODUKT (ukryty przy Leadowanie)
if goal_parent != "Leadowanie":
    with st.container():
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.subheader("Produkt (link)")
        product_url = st.text_input("URL strony produktu", placeholder="https://")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    product_url = ""

# 1E. UWAGI
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    notes = st.text_area("Uwagi (opcjonalnie)")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 2. GENEROWANIE PROMPTU ---------------------------------------------------
st.header("2. Wygeneruj prompt")

if st.button("Generuj brief-prompt"):
    # składanie briefu
    prompt = f"""
Na podstawie poniższych informacji stwórz zwięzły, jasny i konkretny brief dla grafika. Celem briefu jest przygotowanie skutecznej i efektownej kreacji graficznej, dopasowanej do wskazanego celu oraz kanału promocji.

### Parametry z formularza
**Typ materiału:** {material_parent}  
**Kanał / format:** {channel}  
"""
    if channel == "Ulotki":
        prompt += f"**Liczba stron ulotki:** {page_count}\n**Format ulotki:** {sub_format}\n"
    elif channel == "Reklama prasowa":
        prompt += f"**Format reklamy prasowej:** {sub_format}\n"
    elif channel == "Rollup":
        prompt += f"**Format roll-upa:** {sub_format}\n"
    elif sub_format:
        prompt += f"**Format:** {sub_format}\n"

    prompt += f"""**Cel kampanii:** {goal_parent}  
**Opis celu:** {goal_detail}  
"""

    if promotion_text:
        prompt += f"**Treść promocji:** {promotion_text}\n"
    if offer_text:
        prompt += f"**Opis oferty:** {offer_text}\n"
    if lead_magnet:
        prompt += f"**Lead magnet:** {lead_magnet}\n"

    prompt += f"""**Grupa docelowa:** {target_audience}  
**Styl graficzny:** {style}  
**Kolorystyka:** {colorscheme}  
**Elementy obowiązkowe:** {required_elements}  
**CTA:** {cta}  
"""

    if product_url:
        prompt += f"**Link do produktu:** {product_url}\n"
    if notes:
        prompt += f"**Uwagi:** {notes}\n"

    prompt += """
---

Brief powinien zawierać:
1. Podsumowanie kluczowych informacji
2. Propozycje treści (hasła, podtytuły, CTA, bullet points)
3. Zalecenia układu i elementów graficznych
4. Dopasowanie stylistyczne
5. Jeśli materiały to ulotka – strukturę wszystkich stron.

Jeśli masz dostęp do treści pod podanym linkiem, wykorzystaj je do stworzenia treści.
"""
    st.session_state["prompt"] = prompt

# --- 3. EDYCJA I POBRANIE -----------------------------------------------------
if "prompt" in st.session_state:
    st.header("3. Edytuj i pobierz")
    text = st.text_area("Prompt:", st.session_state["prompt"], height=420)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 Pobierz .txt",
            data=text.encode("utf-8"),
            file_name="prompt.txt",
            mime="text/plain",
        )
    with col2:
        st.code(text, language="markdown")
