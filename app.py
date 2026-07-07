import streamlit as st
import google.generativeai as genai

# 1. CONFIGURAZIONE DELLA PAGINA E GRAFICA DI BASE
st.set_page_config(page_title="Regista AI per Docenti", page_icon="🎬", layout="wide")

st.title("🎬 Il Regista Multimediale per Docenti")
st.markdown("Crea la sceneggiatura, i prompt per **Canva** e la colonna sonora su **Pixabay** in pochi clic.")
st.markdown("---")

# 2. CONFIGURAZIONE DELL'API DI GEMINI
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.warning("⚠️ Inserisci la tua chiave API di Gemini nei settings di Streamlit per far funzionare l'app.")

# 3. LE ISTRUZIONI DI SISTEMA (La "Gemma" e la Legenda)
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

# 4. L'INTERFACCIA UTENTE (Step 1 e Step 2)
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

# 5. IL MOTORE DI GENERAZIONE (Step 3 e 4)
if st.button("🚀 Genera Storyboard Completo", type="primary"):
    if argomento:
        with st.spinner("Sto analizzando il sistema e scrivendo la sceneggiatura..."):
            try:
                # IL RADAR: Cerchiamo il nome esatto del modello autorizzato sulla tua API Key
                modello_corretto = "gemini-1.5-flash" # Nome di emergenza di base
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        if '1.5-flash' in m.name:
                            modello_corretto = m.name
                            break
                
                # Inizializziamo il modello con il nome esatto trovato dal radar
                model = genai.GenerativeModel(
                    model_name=modello_corretto,
                    system_instruction=istruzioni_regista
                )
                
                # Costruiamo la richiesta
                prompt_utente = f"Argomento: {argomento}\nTarget: {target}\nStile: {stile}\nGenera lo storyboard completo."
                
                # Lanciamo la generazione
                response = model.generate_content(prompt_utente)
                
                # Mostriamo il risultato
                st.success(f"Storyboard generato con successo! (Motore agganciato: {modello_corretto})")
                st.markdown(response.text)
                
            except Exception as e:
                # In caso di errore, lo mostriamo a schermo in modo pulito
                st.error(f"Errore durante l'elaborazione di Gemini: {e}")
                st.info("Se continui a vedere errori, verifica che la tua API Key sia abilitata per i servizi Generative Language API nella console di Google AI Studio.")
    else:
        st.error("Per favore, scrivi l'argomento della lezione prima di procedere.")
