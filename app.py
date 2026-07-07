import streamlit as st
from google import genai
from google.genai import types

# 1. CONFIGURAZIONE DELLA PAGINA E GRAFICA DI BASE
st.set_page_config(page_title="Regista AI per Docenti", page_icon="🎬", layout="wide")

st.title("🎬 Il Regista Multimediale per Docenti")
st.markdown("Crea la sceneggiatura, i prompt per **Canva** e la colonna sonora su **Pixabay** in pochi clic.")
st.markdown("---")

# 2. LE ISTRUZIONI DI SISTEMA (La tua "Gemma" + Legenda)
istruzioni_regista = """
Ruolo: Sei un Regista Multimediale e un Sound Designer esperto in didattica digitale per la scuola.
Il tuo obiettivo è generare uno storyboard usando questa legenda rigida per facilitare i docenti:
- [Minutaggio] V1, V2... = Vignetta / Scena (es. [00:00 - 00:05] V1)
- Prompt CANVA = Prompt esatto in INGLESE per l'AI video (semplice e lineare per evitare errori del motore), inserito ESCLUSIVAMENTE in un blocco di codice markdown copiabile.
- SFX = Fornisci 3 opzioni di keyword in INGLESE per gli effetti sonori. Crea link diretti: https://pixabay.com/it/sound-effects/search/keyword_in_inglese/
- DID/DIAL = Didascalia narrante in italiano.
- NOTE/LAYOUT = Istruzioni pratiche di montaggio e variazioni rispetto alla gabbia standard (es. inquadrature e formati).

Regola Fissa: Inizia sempre con una nota per i docenti spiegando che i prompt visivi e di ricerca sono in inglese per garantire la massima precisione dei motori AI.
"""

# 3. L'INTERFACCIA UTENTE (Step 1 e Step 2)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 1. Chi sono i tuoi studenti?")
    target = st.selectbox(
        "Seleziona il grado scolastico:", 
        ["Scuola Primaria", "Scuola Secondaria di I grado", "Scuola Secondaria di II grado"]
    )

with col2:
    st.subheader("🎨 2. Quale stile visivo preferisci?")
    stile = st.selectbox(
        "Seleziona l'estetica del video:", 
        ["Retro-VHS anni '80", "Documentario Storico Cinematico", "Animazione 2D Cartoon", "Disegno a matita Lo-Fi"]
    )

st.subheader("📚 3. Argomento della Lezione")
argomento = st.text_area("Cosa vuoi spiegare in questo video?", placeholder="Es. L'evoluzione del pianoforte, Il ciclo dell'acqua, La rivoluzione industriale...")

# 4. IL MOTORE DI GENERAZIONE (Nuova Libreria Ufficiale)
if st.button("🚀 Genera Storyboard Completo", type="primary"):
    if argomento:
        with st.spinner("Connessione al nuovo motore Gemini in corso..."):
            try:
                # Inizializziamo il client ufficiale richiamando la chiave nascosta
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                # Costruiamo la richiesta unendo le scelte dell'utente
                prompt_utente = f"Argomento: {argomento}\nTarget: {target}\nStile: {stile}\nGenera lo storyboard completo."
                
                # Lanciamo la generazione con la nuova sintassi
                response = client.models.generate_content(
                    model='gemini-2.0-flash', 
                    contents=prompt_utente,
                    config=types.GenerateContentConfig(
                        system_instruction=istruzioni_regista,
                        temperature=0.7
                    )
                )
                
                # Mostriamo il risultato a schermo
                st.success("Storyboard generato con successo!")
                st.markdown(response.text)
                
            except KeyError:
                st.error("⚠️ Chiave API non trovata! Assicurati di aver incollato la chiave nei 'Secrets' di Streamlit.")
            except Exception as e:
                st.error(f"Errore durante l'elaborazione di Gemini: {e}")
    else:
        st.error("Per favore, scrivi l'argomento della lezione prima di procedere.")
