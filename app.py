import streamlit as st
import google.generativeai as genai

# 1. CONFIGURAZIONE DELLA PAGINA E GRAFICA DI BASE
st.set_page_config(page_title="Regista AI per Docenti", page_icon="🎬", layout="wide")

st.title("🎬 Il Regista Multimediale per Docenti")
st.markdown("Crea la sceneggiatura, i prompt per **Canva** e la colonna sonora su **Pixabay** in pochi clic.")
st.markdown("---")

# 2. CONFIGURAZIONE DELL'API DI GEMINI
# In produzione su Streamlit Cloud, la chiave API verrà presa dai "Secrets" in modo sicuro.
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.warning("⚠️ Inserisci la tua chiave API di Gemini nei settings di Streamlit per far funzionare l'app.")

# 3. LE ISTRUZIONI DI SISTEMA (La tua "Gemma" + Legenda)
# Questo testo è il cervello dell'app, invisibile ai docenti ma letto dall'AI.
istruzioni_regista = """
Ruolo: Sei un Regista Multimediale e un Sound Designer esperto in didattica digitale.
Il tuo obiettivo è generare uno storyboard usando questa legenda rigida:
- V1, V2... = Vignetta / Scena e minutaggio stimato (es. [00:00 - 00:05] V1)
- Prompt CANVA = Prompt in INGLESE per l'AI video (semplice e lineare), racchiuso in un blocco di codice markdown copiabile.
- SFX = Fornisci 3 opzioni di keyword in INGLESE per gli effetti sonori. Per ogni opzione crea un link del tipo: https://pixabay.com/it/sound-effects/search/keyword_in_inglese/
- DID/DIAL = Didascalia narrante in italiano.
- NOTE/LAYOUT = Istruzioni di montaggio pratiche per la timeline.

Regola Fissa: Inizia sempre la risposta con una breve nota che spiega che i prompt sono in inglese per garantire la massima precisione dei motori AI. Non generare nient'altro fuori da questo schema.
"""

# Inizializziamo il modello Gemini 1.5 Flash (veloce e supporta le istruzioni di sistema)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    system_instruction=istruzioni_regista
)

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
argomento = st.text_area("Cosa vuoi spiegare in questo video?", placeholder="Es. Le regole del contrappunto, La struttura della cellula, La rivoluzione industriale...")

# 5. IL MOTORE DI GENERAZIONE (Step 3 e 4)
if st.button("🚀 Genera Storyboard Completo", type="primary"):
    if argomento:
        with st.spinner("Sto scrivendo la sceneggiatura e preparando i prompt visivi e sonori..."):
            
            # Uniamo le scelte dell'utente in un unico comando per Gemini
            prompt_utente = f"Argomento: {argomento}\nTarget: {target}\nStile: {stile}\nGenera lo storyboard completo rispettando le regole."
            
            # Chiamata all'API
            response = model.generate_content(prompt_utente)
            
            # Mostriamo il risultato a schermo
            st.success("Storyboard generato con successo! Copia i prompt qui sotto.")
            st.markdown(response.text)
    else:
        st.error("Per favore, scrivi l'argomento della lezione prima di procedere.")
