import streamlit as st
from collections import Counter
import matplotlib.pyplot as plt
import base64
import streamlit.components.v1 as components

# ------------------- PAGE SETUP ---------------------
st.set_page_config(page_title="SeqVerse - Bioinformatics Toolkit", layout="wide")

# Background Styling
background_url = "https://www.icgeb.org/wp-content/uploads/2023/01/Genomic-analysis-488977381.png"
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('{background_url}');
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
    }}
    .white-text, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
        color: white !important;
    }}
    div[data-testid="stMarkdownContainer"] > p {{
        color: white !important;
    }}
    .result-box {{
        background-color: rgba(0, 0, 0, 0.6);
        color: white;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 10px;
    }}
    .highlight-box {{
        background: linear-gradient(90deg, #e3ffe7 0%, #d9e7ff 100%);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# ------------------- APP TITLE ---------------------
st.markdown("<h1 class='white-text'>🧬 SeqVerse</h1>", unsafe_allow_html=True)

# ------------------- TABS ---------------------
tabs = st.tabs(["🏠 Home", "🧪 Tool", "ℹ️ About"])

# ------------------- HOME TAB ---------------------
with tabs[0]:
    st.markdown("## Welcome to SeqVerse")
    st.markdown("""
    <div class='white-text'>
    <strong>SeqVerse</strong> is an interactive bioinformatics toolkit built to empower students and researchers in decoding genetic data.  
    
    This toolkit enables real-time <strong>DNA analysis</strong>, <strong>transcription</strong>, <strong>translation</strong>, and visualization of important genomic features.

    <h3>🎯 Objectives:</h3>
    <ul>
        <li>Provide an intuitive interface for basic sequence analysis</li>
        <li>Enable conversion of DNA → RNA → Protein</li>
        <li>Integrate visualizations and download options</li>
        <li>Link to external tools like AlphaFold and UniProt</li>
    </ul>

    <h3>🔧 Key Features:</h3>
    <ul>
        <li>GC & AT Content analysis</li>
        <li>Reverse complement generation</li>
        <li>Codon usage statistics</li>
        <li>Transcription & protein translation</li>
        <li>Downloadable result summaries</li>
        <li>External tool integration</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)


# ------------------- TOOL TAB ---------------------
with tabs[1]:
    st.markdown("## 📥 DNA Sequence Input")

    # Custom styles
    st.markdown("""
        <style>
        /* Gradient background for textarea */
        section[data-testid="stTextArea"] textarea {
            background: linear-gradient(135deg, #a1ffce 0%, #faffd1 100%) !important;
            border-radius: 10px !important;
            border: 2px solid #00d4ff !important;
            color: black !important;
            font-weight: bold !important;
        }

        /* Style the button: force black text */
        div.stButton > button {
            color: black !important;
            font-weight: bold;
            background-color: #d1faff; /* Optional: soft cyan background */
            border: 1px solid #00d4ff;
        }
        </style>
    """, unsafe_allow_html=True)

    # Input and button
    dna_input = st.text_area("Paste your DNA sequence (A, T, G, C only):", height=150).upper()
    run_analysis = st.button("▶️ Run Analysis", use_container_width=True)

    def clean_sequence(seq):
        return ''.join([base for base in seq if base in ['A', 'T', 'G', 'C']])

    def reverse_complement(seq):
        complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        return ''.join([complement[base] for base in reversed(seq)])

    def get_codon_usage(seq):
        codons = [seq[i:i+3] for i in range(0, len(seq)-2, 3)]
        return dict(sorted(Counter(codons).items()))

    def transcribe(seq):
        transcription_map = {'A': 'U', 'T': 'A', 'G': 'C', 'C': 'G'}
        return ''.join([transcription_map[base] for base in seq])

    def translate(rna):
        codon_table = {
            "UUU": "F", "CUU": "L", "AUU": "I", "GUU": "V", "UUC": "F", "CUC": "L", "AUC": "I", "GUC": "V",
            "UUA": "L", "CUA": "L", "AUA": "I", "GUA": "V", "UUG": "L", "CUG": "L", "AUG": "M", "GUG": "V",
            "UCU": "S", "CCU": "P", "ACU": "T", "GCU": "A", "UCC": "S", "CCC": "P", "ACC": "T", "GCC": "A",
            "UCA": "S", "CCA": "P", "ACA": "T", "GCA": "A", "UCG": "S", "CCG": "P", "ACG": "T", "GCG": "A",
            "UAU": "Y", "CAU": "H", "AAU": "N", "GAU": "D", "UAC": "Y", "CAC": "H", "AAC": "N", "GAC": "D",
            "UAA": "STOP", "CAA": "Q", "AAA": "K", "GAA": "E", "UAG": "STOP", "CAG": "Q", "AAG": "K", "GAG": "E",
            "UGU": "C", "CGU": "R", "AGU": "S", "GGU": "G", "UGC": "C", "CGC": "R", "AGC": "S", "GGC": "G",
            "UGA": "STOP", "CGA": "R", "AGA": "R", "GGA": "G", "UGG": "W", "CGG": "R", "AGG": "R", "GGG": "G"
        }
        protein = ""
        for i in range(0, len(rna), 3):
            codon = rna[i:i+3]
            if codon in codon_table:
                aa = codon_table[codon]
                if aa == "STOP":
                    break
                protein += aa
        return protein


    if dna_input:
        dna = clean_sequence(dna_input)

        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        with st.expander("📊 DNA Analysis", expanded=True):
            st.markdown(f"<div class='result-box'>Length: {len(dna)} bp</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='result-box'>GC Content: {100 * (dna.count('G') + dna.count('C')) / len(dna):.2f}%</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='result-box'>AT Content: {100 * (dna.count('A') + dna.count('T')) / len(dna):.2f}%</div>", unsafe_allow_html=True)
            st.code("Reverse Complement:\n" + reverse_complement(dna))
            st.markdown("<h4 class='white-text'>🧬 Codon Usage</h4>", unsafe_allow_html=True)
            codon_usage = get_codon_usage(dna)
            fig, ax = plt.subplots(figsize=(10, 3))
            ax.bar(codon_usage.keys(), codon_usage.values(), color='orange')
            plt.xticks(rotation=90)
            st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        with st.expander("🔄 Transcription & Translation", expanded=True):
            rna = transcribe(dna)
            protein = translate(rna)
            st.markdown(f"<div class='result-box'><b>RNA Sequence:</b><br>{rna}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='result-box'><b>Protein Sequence:</b><br>{protein}</div>", unsafe_allow_html=True)
            if protein:
                acidic = sum(1 for aa in protein if aa in {'D', 'E'})
                basic = sum(1 for aa in protein if aa in {'R', 'K', 'H'})
                st.markdown(f"<div class='result-box'>Acidic AAs (%): {acidic / len(protein) * 100:.2f}%</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='result-box'>Basic AAs (%): {basic / len(protein) * 100:.2f}%</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("### 🔗 External Tools")
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image("https://www.blog.crownet.net/wp-content/uploads/2024/10/AlphaFold-1024x605.png", width=60)
        with col2:
            st.markdown("<h4 style='color:white;'>AlphaFold Structure Prediction</h4>", unsafe_allow_html=True)
            st.info("Copy the translated protein sequence and paste it into the AlphaFold server.")
            st.markdown("""
                <a href="https://alphafoldserver.com/" target="_blank">
                    <button style="background-color:white; color:black; padding:8px 16px; border-radius:8px; border:none; font-weight:bold;">Open AlphaFold</button>
                </a>
            """, unsafe_allow_html=True)

        st.markdown("### 🧬 UniProt BLAST")
        st.info("Paste the protein sequence into UniProt BLAST to identify matching proteins.")
        components.iframe("https://www.uniprot.org/blast/", height=800, scrolling=True)

        def create_download_link(text, filename="SeqVerse_Results.txt"):
            b64 = base64.b64encode(text.encode()).decode()
            return f'''
                <a href="data:text/plain;base64,{b64}" download="{filename}">
                    <button style="background-color:white; color:black; font-weight:bold; padding:10px 20px; border:none; border-radius:8px; cursor:pointer;">
                        📄 Download Results
                    </button>
                </a>
            '''

        output_text = f"""SeqVerse Bioinformatics Results

DNA Sequence (Cleaned):
{dna}

RNA Sequence:
{rna}

Protein Sequence:
{protein}

Reverse Complement:
{reverse_complement(dna)}

GC Content: {100 * (dna.count('G') + dna.count('C')) / len(dna):.2f}%
AT Content: {100 * (dna.count('A') + dna.count('T')) / len(dna):.2f}%

Codon Usage:
"""
        for codon, count in codon_usage.items():
            output_text += f"{codon}: {count}\n"
        if protein:
            output_text += f"Acidic AAs (%): {acidic / len(protein) * 100:.2f}%\n"
            output_text += f"Basic AAs (%): {basic / len(protein) * 100:.2f}%\n"

        st.markdown(create_download_link(output_text), unsafe_allow_html=True)

# ------------------- ABOUT TAB ---------------------
with tabs[2]:
    
    st.markdown("""
        <div style='text-align: center;'>
            <img src='https://media.licdn.com/dms/image/v2/D4D03AQFkAXfmVgs4tw/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1730916040029?e=1752105600&v=beta&t=kKi12reIJ9NH2sCn1VxV5ipMYB7E5N0fSNtacgi29_0' 
                 width='150' style='border-radius: 50%; margin-bottom: 10px;'>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("## 👨‍💻 About SeqVerse", unsafe_allow_html=True)
    st.markdown("""
    <div class='white-text'>

    **SeqVerse** is a bioinformatics toolkit designed and developed by Apurva Waduskar, currently pursuing an MSc in Bioinformatics at DES Pune University, Maharashtra, India.  
    This platform was conceptualized and created as part of an academic mini-project to deliver an accessible, browser-based solution for genetic sequence analysis.

    ### 🎯 Purpose
    - Provide a real-time, user-friendly tool for DNA and protein sequence analysis  
    - Simplify transcription, translation, and GC content computation  
    - Empower students and researchers with essential bioinformatics tools without needing command-line setups

    ### 🔑 Key Features 
    🧬 DNA to RNA Transcription and Protein Translation  
    📈 GC and AT Content Calculation  
    🔄 Reverse Complement Sequence Generator  
    🧬 Codon Usage Table and Frame-wise Translation  
    🔍 UniProt Link Integration via REST API  

    ### ⚙️ Tools & Technologies Used  
    - Python and Streamlit for app development  
    - Biopython for sequence operations and analysis  
    - Matplotlib and Seaborn for plotting visualizations  
    - UniProt REST API for retrieving protein information  
    - AlphaFold Database for viewing predicted protein 3D structures

    ### 💡 Benefits
    - No installation needed – fully browser-based  
    - Beginner-friendly interface with intuitive input/output  
    - Educational tool to demonstrate core bioinformatics concepts  
    - Modular structure allows for easy addition of future features and tools 

    ### 🚀 Future Enhancements
    - Integration with Pfam or InterPro for domain annotation  
    - GC Skew Plot for replication origin detection  
    - Restriction enzyme cut site analysis using REBASE  
    - Protein feature visualizations (e.g., transmembrane regions, signal peptides)  
    - Save and export session summaries and plots

    ### 👨‍🏫 Acknowledgements
    Special thanks to the faculty at DES Pune University for their guidance and support throughout this project.

    ### 🔗 Connect
    - 📧 Email: [waduskarapurva@gmail.com]  
    - 💼 LinkedIn: [www.linkedin.com/in/apurva-waduskar-ab4079286]  
    - 💻 GitHub: [https://github.com/Apurva-Waduskar]

    </div>
    """, unsafe_allow_html=True)

