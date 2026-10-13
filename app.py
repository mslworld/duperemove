import streamlit as st
import pandas as pd
import os
from collections import Counter
import io

# USA Area Codes Mapping for State Detection
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

# Session State Initialization
def init_session():
    if 'seen_numbers' not in st.session_state:
        st.session_state.seen_numbers = set()
    if 'state_counts' not in st.session_state:
        st.session_state.state_counts = Counter()
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = 0

def clear_session():
    st.session_state.seen_numbers = set()
    st.session_state.state_counts = Counter()
    st.session_state.processed_files = 0
    if os.path.exists(INVALID_FILE_PATH):
        os.remove(INVALID_FILE_PATH)

st.set_page_config(page_title="Ultra-Fast Phone Deduplicator", layout="wide")
init_session()

st.title("🚀 Ultra-Fast Sequential Number Deduplicator")
st.markdown("Upload files back-to-back. 10-digit valid US numbers filter honge, aur pichli saari files ke against deduplicate honge.")

col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"**Files Processed:** {st.session_state.processed_files}")
with col2:
    st.success(f"**Total Unique Numbers (Session):** {len(st.session_state.seen_numbers)}")
with col3:
    if st.button("🗑️ Clear Entire Session", use_container_width=True):
        clear_session()
        st.rerun()

uploaded_file = st.file_uploader("Upload Phone Numbers File (CSV/TXT - Up to 1GB+)", type=['csv', 'txt'])

if uploaded_file is not None:
    st.markdown("---")
    with st.spinner("Processing file at extreme speed..."):
        
        valid_unique_list = []
        chunk_size = 500000 # 5 lakh rows per chunk taki RAM crash na ho
        
        # Read file in chunks to handle 1GB+ files seamlessly
        for chunk in pd.read_csv(uploaded_file, chunksize=chunk_size, header=None, names=['raw_phone'], dtype=str, encoding='utf-8', on_bad_lines='skip'):
            
            # Drop nulls
            chunk = chunk.dropna(subset=['raw_phone'])
            
            # Clean numbers: Remove all non-digits (spaces, dashes, brackets)
            chunk['clean'] = chunk['raw_phone'].str.replace(r'\D', '', regex=True)
            
            # Validation: Must be exactly 10 digits
            is_valid = chunk['clean'].str.len() == 10
            
            valid_chunk = chunk[is_valid].copy()
            invalid_chunk = chunk[~is_valid]
            
            # 1. Append Invalid numbers to disk (Saves RAM)
            if not invalid_chunk.empty:
                invalid_chunk[['raw_phone']].to_csv(INVALID_FILE_PATH, mode='a', index=False, header=False)
            
            # 2. Deduplicate valid numbers
            if not valid_chunk.empty:
                # Remove duplicates within the current chunk first
                valid_chunk = valid_chunk.drop_duplicates(subset=['clean'])
                
                # Filter against GLOBAL seen numbers
                # ~ (NOT in seen_numbers)
                unique_mask = ~valid_chunk['clean'].isin(st.session_state.seen_numbers)
                new_unique_chunk = valid_chunk[unique_mask]
                
                if not new_unique_chunk.empty:
                    # Extract pure numbers list
                    new_numbers = new_unique_chunk['clean'].tolist()
                    
                    # Update global memory
                    st.session_state.seen_numbers.update(new_numbers)
                    
                    # Store for this specific file's output
                    valid_unique_list.extend(new_numbers)
                    
                    # Update State Statistics
                    area_codes = new_unique_chunk['clean'].str[:3]
                    states = area_codes.map(AREA_CODES).fillna('Unknown')
                    st.session_state.state_counts.update(states.tolist())

        st.session_state.processed_files += 1
        
        # Create output files in memory for fast download
        df_output = pd.DataFrame(valid_unique_list, columns=['Valid_Unique_Numbers'])
        csv_output = df_output.to_csv(index=False).encode('utf-8')
        
        st.success(f"✅ Processing Complete! Found **{len(valid_unique_list)}** new unique 10-digit numbers in this file.")
        
        # Download Section
        st.subheader("📥 Download Results")
        col_dl1, col_dl2 = st.columns(2)
        
        with col_dl1:
            st.download_button(
                label="Download Unique Numbers (For this file)",
                data=csv_output,
                file_name=f"Cleaned_{uploaded_file.name}",
                mime="text/csv",
                use_container_width=True
            )
            
        with col_dl2:
            if os.path.exists(INVALID_FILE_PATH):
                with open(INVALID_FILE_PATH, "rb") as f:
                    st.download_button(
                        label="Download All Invalid Numbers (Session)",
                        data=f,
                        file_name="All_Invalid_Numbers.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
        
        # Reports Section
        st.markdown("---")
        st.subheader("📊 US States Report (Active Session)")
        if st.session_state.state_counts:
            # Convert Counter to DataFrame for Streamlit charting
            state_df = pd.DataFrame.from_dict(st.session_state.state_counts, orient='index').reset_index()
            state_df.columns = ['State', 'Count']
            state_df = state_df.sort_values(by='Count', ascending=False)
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.dataframe(state_df, hide_index=True, use_container_width=True)
            with c2:
                st.bar_chart(state_df.set_index('State'))