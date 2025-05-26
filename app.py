# app.py
import streamlit as st
from io import StringIO

st.set_page_config(page_title="Brief Generator", layout="centered")

st.title("Generator promptów do briefów graficznych")

# --- 1. FORMULARZ -------------------------------------------------------------
st.header("1. Wypełnij formularz")

# Typ materiału
material_parent = st.radio("Typ materiałów",
                           ["Grafiki reklamowe", "Materiały drukowane"])

if material_parent == "Grafiki reklamowe":
    channel = st.radio("Kanał", ["Facebook", "Google Ads", "Mail",
                                 "Strona www", "Inne"])
    if channel == "Inne":
        channel = st.text_input("Podaj kanał / format")
    # Dodatkowe pola specyficzne tu nie są potrzebne
    page_count = None
    sub_format = None

else:  # Materiały drukowane
    channel = st.radio("Format drukowany",
                       ["Ulotki", "Reklama prasowa", "Rollup", "Inne"])
    if channel == "Ulotki":
        page_count = st.number_input("Ilość stron ulotki", min_value=1, value=2)
        sub_format = st.text_input("Format ulotki (np. A5, DL, custom)")
    elif channel == "Reklama prasowa":
        sub_format = st.radio("Format reklamy",
                              ["1 strona", "½ strony pionowo",
                               "½ strony poziomo", "Inny"])
        if sub_format == "Inny":
            sub_format = st.text_input("Podaj format")
        page_count = None
    elif channel == "Rollup":
        sub_format = st.radio("Format roll-upa", ["85x200", "100x200"])
        page_count = None
    else:  # Inne
        sub_format = st.text_input("Podaj format")
        page_count = None

# Cel
goal_parent = st.radio("Cel",
                       ["Sprzedaż", "Leadowanie", "Inne"])
if goal_parent == "Sprzedaż":
    goal_detail = st.radio("Konkretny cel sprzedażowy",
                           ["Zachęcenie do zakupu",
                            "Promocja nowego produktu",
                            "Przedstawienie rabatu / oferty specjalnej"])
elif goal_parent == "Leadowanie":
    goal_detail = st.radio("Konkretny cel leadowy",
                           ["Pobranie materiału (ebook, PDF, raport)",
                            "Zapis na webinar / wydarzenie"])
else:
    goal_detail = st.text_input("Opisz cel")

# CTA
cta_parent = st.radio("Preferowane CTA",
                      ["Sprzedaż", "Leadowanie", "Inne"])
if cta_parent == "Sprzedaż":
    cta = st.radio("CTA sprzedażowe",
                   ["Kup teraz", "Zamów dziś", "Skorzystaj z promocji",
                    "Odbierz zniżkę"])
elif cta_parent == "Leadowanie":
    cta = st.radio("CTA leadowe",
                   ["Zapisz się", "Dołącz do nas", "Pobierz za darmo",
                    "Odbierz materiał"])
else:
    cta = st.text_input("Wpisz CTA")

# Pozostałe pola
target_audience = st.text_input("Grupa docelowa")
colorscheme_radio = st.radio("Kolorystyka",
                             ["zgodna z KV produktu / marki produktu",
                              "inna"])
if colorscheme_radio == "inna":
    colorscheme = st.text_input("Opisz kolorystykę")
else:
    colorscheme = colorscheme_radio

required_elements = st.multiselect("Niezbędne elementy",
                                   ["logo", "informacja o promocji"])
required_elements_extra = st.text_input("Inne elementy (opcjonalnie)")
if required_elements_extra:
    required_elements.append(required_elements_extra)
required_elements = ", ".join(required_elements) if required_elements else "brak"

style_radio = st.radio("Styl graficzny",
                       ["Minimalistyczny", "Profesjonalny", "Nowoczesny",
                        "Futurystyczny", "Technologiczny", "Emocjonalny",
                        "Luksusowy", "Casualowy – lekki", "Inny"])
if style_radio == "Inny":
    style = st.text_input("Opisz styl")
else:
    style = style_radio

product_url = st.text_input("Link do strony produktu", placeholder="https://")

# --- 2. GENEROWANIE PROMPTU ---------------------------------------------------
st.header("2. Wygeneruj prompt")

if st.button("Generuj"):
    prompt_template = f"""
Na podstawie poniższych informacji stwórz zwięzły, jasny i konkretny brief dla grafika. Celem briefu jest przygotowanie skutecznej i efektownej kreacji graficznej, dopasowanej do wskazanego celu oraz kanału promocji.
Brief powinien zawierać:
1. Podsumowanie kluczowych informacji umieszczonych w formularzu
2. Propozycje treści do umieszczenia na grafikach:
   - hasło główne (2-3 propozycje)
   - tekst pomocniczy / podtytuł (2-3 propozycje)
   - CTA (2-3 propozycje)
   - 3–5 bullet points (opcjonalnie) (1 wersja)
   - ewentualne dodatkowe treści jeśli format projektu na to pozwala / tego wymaga
3. Zalecenia co do układu i elementów graficznych
4. Dostosowanie stylistyki do stylu marki lub zdefiniowanego w formularzu.
5. Jeśli materiałem jest **ulotka** – zaproponuj **strukturę i zawartość wszystkich stron**, zgodnie z podaną liczbą.

### Parametry z formularza
**Typ materiału graficznego:** {material_parent}  
**Kanał / format:** {channel}  
"""
    # wstawianie dodatkowych parametrów zależnie od kanału
    if channel == "Ulotki":
        prompt_template += f"**Liczba stron ulotki:** {page_count}\n**Format ulotki:** {sub_format}\n"
    elif channel == "Reklama prasowa":
        prompt_template += f"**Format reklamy prasowej:** {sub_format}\n"
    elif channel == "Rollup":
        prompt_template += f"**Format roll-upa:** {sub_format}\n"
    elif sub_format:
        prompt_template += f"**Format:** {sub_format}\n"

    prompt_template += f"""
**Cel kampanii:** {goal_parent}  
**Opis celu (szczegółowo):** {goal_detail}  
**Grupa docelowa:** {target_audience}  
**Styl graficzny:** {style}  
**Kolorystyka:** {colorscheme}  
**Elementy obowiązkowe:** {required_elements}  
**Preferowane CTA:** {cta}  
**Link do strony produktowej:** {product_url}

---
Na podstawie powyższych danych przygotuj zwięzły i atrakcyjny brief + propozycje treści reklamowej.  
Zadbaj, by komunikaty były dopasowane do celu ({goal_parent}), formatu ({channel}), stylu ({style}) i grupy docelowej ({target_audience}).

Pamiętaj, że:
- Grafika powinna być przejrzysta, skuteczna i dostosowana do kanału emisji.
- CTA powinno być mocne, jednoznaczne i powiązane z celem.
- Hasło reklamowe musi przyciągać uwagę i wywoływać emocje.
- Jeśli to materiał drukowany, zaplanuj układ treści przestrzennie.

Jeśli masz dostęp do treści pod adresem {product_url}, wykorzystaj ją do przygotowania treści – zidentyfikuj kluczowe cechy, przewagi, język komunikacji i najważniejsze informacje produktowe.
"""
    st.session_state["prompt"] = prompt_template

# --- 3. EDYCJA I POBRANIE -----------------------------------------------------
if "prompt" in st.session_state:
    st.header("3. Edytuj i zapisz prompt")
    text = st.text_area("Prompt:", st.session_state["prompt"], height=400)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Pobierz jako .txt",
                           data=text.encode("utf-8"),
                           file_name="prompt.txt",
                           mime="text/plain")
    with col2:
        st.code(text, language="markdown")
        st.caption("Zaznacz i skopiuj ręcznie, jeśli wolisz.")
