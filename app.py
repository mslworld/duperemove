import streamlit as st
import pandas as pd
import numpy as np
import os
from collections import Counter

# USA Area Codes Mapping
AREA_CODES = {
    '201': 'NJ', '202': 'DC', '203': 'CT', '205': 'AL', '206': 'WA', '207': 'ME', '208': 'ID', '209': 'CA',
    '210': 'TX', '212': 'NY', '213': 'CA', '214': 'TX', '215': 'PA', '216': 'OH', '217': 'IL', '218': 'MN',
    '219': 'IN', '224': 'IL', '225': 'LA', '228': 'MS', '229': 'GA', '231': 'MI', '234': 'OH', '239': 'FL',
    '240': 'MD', '248': 'MI', '251': 'AL', '252': 'NC', '253': 'WA', '254': 'TX', '256': 'AL', '260': 'IN',
    '262': 'WI', '267': 'PA', '269': 'MI', '270': 'KY', '276': 'VA', '281': 'TX', '301': 'MD', '302': 'DE',
    '303': 'CO', '304': 'WV', '305': 'FL', '307': 'WY', '308': 'NE', '309': 'IL', '310': 'CA', '312': 'IL',
    '313': 'MI', '314': 'MO', '315': 'NY', '316': 'KS', '317': 'IN', '318': 'LA', '319': 'IA', '320': 'MN',
    '321': 'FL', '323': 'CA', '325': 'TX', '330': 'OH', '334': 'AL', '336': 'NC', '337': 'LA', '339': 'MA',
    '347': 'NY', '351': 'MA', '352': 'FL', '360': 'WA', '361': 'TX', '386': 'FL', '401': 'RI', '402': 'NE',
    '404': 'GA', '405': 'OK', '406': 'MT', '407': 'FL', '408': 'CA', '409': 'TX', '410': 'MD', '412': 'PA',
    '413': 'MA', '414': 'WI', '415': 'CA', '417': 'MO', '419': 'OH', '423': 'TN', '424': 'CA', '425': 'WA',
    '430': 'TX', '432': 'TX', '434': 'VA', '435': 'UT', '440': 'OH', '443': 'MD', '469': 'TX', '478': 'GA',
    '479': 'AR', '480': 'AZ', '484': 'PA', '501': 'AR', '502': 'KY', '503': 'OR', '504': 'LA', '505': 'NM',
    '507': 'MN', '508': 'MA', '509': 'WA', '510': 'CA', '512': 'TX', '513': 'OH', '515': 'IA', '516': 'NY',
    '517': 'MI', '518': 'NY', '520': 'AZ', '530': 'CA', '540': 'VA', '541': 'OR', '551': 'NJ', '559': 'CA',
    '561': 'FL', '562': 'CA', '563': 'IA', '567': 'OH', '570': 'PA', '571': 'VA', '573': 'MO', '574': 'IN',
    '580': 'OK', '585': 'NY', '586': 'MI', '601': 'MS', '602': 'AZ', '603': 'NH', '605': 'SD', '607': 'NY',
    '608': 'WI', '609': 'NJ', '610': 'PA', '612': 'MN', '614': 'OH', '615': 'TN', '616': 'MI', '617': 'MA',
    '618': 'IL', '619': 'CA', '620': 'KS', '623': 'AZ', '626': 'CA', '630': 'IL', '631': 'NY', '636': 'MO',
    '641': 'IA', '646': 'NY', '650': 'CA', '651': 'MN', '660': 'MO', '661': 'CA', '662': 'MS', '678': 'GA',
    '682': 'TX', '701': 'ND', '702': 'NV', '703': 'VA', '704': 'NC', '706': 'GA', '707': 'CA', '708': 'IL',
    '712': 'IA', '713': 'TX', '714': 'CA', '715': 'WI', '716': 'NY', '717': 'PA', '718': 'NY', '719': 'CO',
    '720': 'CO', '724': 'PA', '727': 'FL', '732': 'NJ', '734': 'MI', '740': 'OH', '757': 'VA', '760': 'CA',
    '763': 'MN', '765': 'IN', '770': 'GA', '772': 'FL', '773': 'IL', '774': 'MA', '775': 'NV', '781': 'MA',
    '785': 'KS', '786': 'FL', '787': 'PR', '801': 'UT', '802': 'VT', '803': 'SC', '804': 'VA', '805': 'CA',
    '806': 'TX', '808': 'HI', '810': 'MI', '812': 'IN', '813': 'FL', '814': 'PA', '815': 'IL', '816': 'MO',
    '817': 'TX', '818': 'CA', '828': 'NC', '830': 'TX', '831': 'CA', '832': 'TX', '843': 'SC', '845': 'NY',
    '847': 'IL', '850': 'FL', '856': 'NJ', '858': 'CA', '859': 'KY', '860': 'CT', '862': 'NJ', '863': 'FL',
    '864': 'SC', '865': 'TN', '866': 'Toll-Free', '901': 'TN', '903': 'TX', '904': 'FL', '906': 'MI', '907': 'AK',
    '908': 'NJ', '909': 'CA', '910': 'NC', '912': 'GA', '913': 'KS', '914': 'NY', '915': 'TX', '916': 'CA',
    '917': 'NY', '918': 'OK', '919': 'NC', '920': 'WI', '925': 'CA', '931': 'TN', '936': 'TX', '937': 'OH',
    '940': 'TX', '941': 'FL', '949': 'CA', '952': 'MN', '954': 'FL', '956': 'TX', '970': 'CO', '971': 'OR',
    '972': 'TX', '973': 'NJ', '978': 'MA', '979': 'TX', '980': 'NC', '985': 'LA', '989': 'MI'
}

INVALID_FILE_PATH = "invalid_numbers_session.csv"

st.set_page_config(page_title="Ultra-Fast Sequential Deduplicator", layout="wide")

# Persistent Session State initialize karna
if 'global_seen_numbers' not in st.session_state:
    st.session_state.global_seen_numbers = set()
if 'state_counts' not in st.session_state:
    st.session_state.state_counts = Counter()
if 'file_results' not in st.session_state:
    st.session_state.file_results = {}

def clear_session():
    st.session_state.global_seen_numbers = set()
    st.session_state.state_counts = Counter()
    st.session_state.file_results = {}
    if os.path.exists(INVALID_FILE_PATH):
        os.remove(INVALID_FILE_PATH)

st.title("🚀 Strict Sequential Number Deduplicator")
st.markdown("Multiple files upload karein, unko ID (Order) dein, aur **Process** par click karein. Files usi sequence mein deduplicate hongi (File 2 deduplicates against File 1, File 3 deduplicates against 1 & 2).")

col1, col2 = st.columns([3, 1])
with col1:
    st.success(f"**Total Global Unique Numbers in Active Session:** {len(st.session_state.global_seen_numbers)}")
with col2:
    if st.button("🗑️ Clear Session Data", use_container_width=True):
        clear_session()
        st.rerun()

# Multiple Files Uploader
uploaded_files = st.file_uploader("Upload Phone Numbers Files (CSV/TXT)", type=['csv', 'txt'], accept_multiple_files=True)

if uploaded_files:
    st.markdown("---")
    st.subheader("🔢 Assign Order (Strict Sequence)")
    st.info("Jis file ka order 1 hai, wo sabse pehle process hogi aur base banegi. Order 2 uske against check hogi aur bache hue naye numbers base mein add honge. Order 3 dono ke against check hogi, etc.")
    
    file_order_data = []
    
    for i, file in enumerate(uploaded_files):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.write(f"📄 **{file.name}**")
        with c2:
            order = st.number_input("Order", min_value=1, value=i+1, key=f"order_{file.name}", label_visibility="collapsed")
            
        file_order_data.append({'file_obj': file, 'name': file.name, 'order': order})

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("⚙️ Process Files Strictly in Sequence", type="primary", use_container_width=True):
        
        # Files ko user ke order ke hisaab se sort karna zaroori hai sequence ke liye
        file_order_data.sort(key=lambda x: x['order'])
        
        with st.spinner("Processing files sequence-wise and deduplicating..."):
            
            for item in file_order_data:
                file = item['file_obj']
                file_name = item['name']
                file.seek(0)
                
                valid_unique_list = []
                
                # Chunk size chota rakha hai taake RAM mein masla na aye (1GB file k liye best)
                for chunk in pd.read_csv(file, chunksize=500000, header=None, names=['raw_line'], usecols=[0], dtype=str, encoding='utf-8', on_bad_lines='skip'):
                    chunk = chunk.dropna()
                    
                    # 1. Clean non-digits
                    clean_series = chunk['raw_line'].astype(str).str.replace(r'\D', '', regex=True)
                    
                    # 2. USA Country Code check (Remove leading 1 if total len is 11)
                    cond = (clean_series.str.len() == 11) & (clean_series.str.startswith('1'))
                    chunk['clean'] = np.where(cond, clean_series.str[1:], clean_series)
                    
                    # 3. Valid Length Check (Exactly 10)
                    is_valid = chunk['clean'].str.len() == 10
                    
                    valid_chunk = chunk[is_valid].copy()
                    invalid_chunk = chunk[~is_valid]
                    
                    # Append invalid
                    if not invalid_chunk.empty:
                        invalid_chunk[['raw_line']].to_csv(INVALID_FILE_PATH, mode='a', index=False, header=False)
                        
                    if not valid_chunk.empty:
                        # 4. Intra-chunk Deduplication (Ek hi chunk k andar ke duplicates khatam karo)
                        valid_chunk = valid_chunk.drop_duplicates(subset=['clean'])
                        
                        # 5. Inter-file & Inter-chunk Deduplication (Pichli saari files + ab tak ke purane chunks k khilaf check karo)
                        # MAGIC HAPPENS HERE: strictly filter against ALL previously seen numbers
                        mask = ~valid_chunk['clean'].isin(st.session_state.global_seen_numbers)
                        new_unique_strictly = valid_chunk[mask]
                        
                        if not new_unique_strictly.empty:
                            new_nums = new_unique_strictly['clean'].tolist()
                            
                            # Update lists
                            st.session_state.global_seen_numbers.update(new_nums)
                            valid_unique_list.extend(new_nums)
                            
                            # US States Update
                            states = new_unique_strictly['clean'].str[:3].map(AREA_CODES).fillna('Unknown')
                            st.session_state.state_counts.update(states.tolist())
                
                # Har file completely sequence aur previous saari files ke against clean ho kar is dictionary mein save hogi
                st.session_state.file_results[file_name] = valid_unique_list
                
        st.success("✅ Strict Sequence Deduplication Complete! Ab next block me check karein.")
        st.rerun() # Rerun zaroori tha taake updated sets uper display mein foran show ho jayen

# Download Section (Outside button logic so it persists)
if st.session_state.file_results:
    st.markdown("---")
    st.subheader("📥 Download Processed & Completely Deduplicated Files")
    st.info("Har file pichli saari files ke against deeply clean hui hai. Jo numbers is file me bache hain, wo baaqi kisi uper wali file mein maujood nahi hain.")
    
    for f_name, u_nums in st.session_state.file_results.items():
        df_out = pd.DataFrame(u_nums, columns=['Valid_Unique_Numbers'])
        csv_data = df_out.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label=f"⬇️ Download {f_name} ({len(u_nums)} extremely unique numbers)",
            data=csv_data,
            file_name=f"DeepCleaned_{f_name}",
            mime="text/csv",
            key=f"dl_{f_name}"
        )
        
    if os.path.exists(INVALID_FILE_PATH):
        with open(INVALID_FILE_PATH, "rb") as f:
            st.download_button(
                label="🚨 Download ALL Invalid Numbers (Combined)",
                data=f,
                file_name="All_Invalid_Numbers_Session.csv",
                mime="text/csv"
            )

# US States Report Section
if st.session_state.state_counts:
    st.markdown("---")
    st.subheader("📊 US States Global Stats")
    state_df = pd.DataFrame.from_dict(st.session_state.state_counts, orient='index').reset_index()
    state_df.columns = ['State', 'Count']
    state_df = state_df.sort_values(by='Count', ascending=False)
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.dataframe(state_df, hide_index=True, use_container_width=True)
    with c2:
        st.bar_chart(state_df.set_index('State'))
