import streamlit as st
from fertilizer_recom import FertilizerRecommendation, FertilizerUsed

def app():
    st.markdown("### <span style='color: #01426A;'>Step 1: Recommended Amounts (N-P-K)</span>", unsafe_allow_html=True)
    st.caption('Enter the target amounts of Nitrogen (N), Phosphorus (P), and Potassium (K) for the crop.')

    with st.container(border=True, horizontal=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            recom_N = st.number_input("Recommended N (kg)", min_value=0, max_value=100, value=50, step=10, key="recom_N")
        with col2:
            recom_P = st.number_input("Recommended P (kg)", min_value=0, max_value=100, value=50, step=10, key="recom_P")
        with col3:
            recom_K = st.number_input("Recommended K (kg)", min_value=0, max_value=100, value=50, step=10, key="recom_K")
        
        area_col, _ = st.columns([1, 2])
        with area_col:
            area = st.number_input("Farm Area (ha)", min_value=0.1, value=1.0, step=0.1, key="area")
            
    st.session_state.recom_amount = {'N': recom_N, 'P': recom_P, 'K': recom_K, 'area': float(area)}

    if st.session_state.recom_amount['N'] > 0 or st.session_state.recom_amount['P'] > 0 or st.session_state.recom_amount['K'] > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### <span style='color: #01426A;'>Step 2: Used Fertilizers Overview</span>", unsafe_allow_html=True)
        st.info('Update fertilizer grades in the left sidebar to fulfill these recommended amounts.', icon="ℹ️")

        with st.expander("View current configuration", expanded=False):
            st.code(f"""
# Recommended amounts to fulfill
recom_amount = {st.session_state.recom_amount}

# Fertilizers selected for fulfillment
used_fertilizer_for_Nitrogen = {st.session_state.fert_N}
used_fertilizer_for_Phosphorus = {st.session_state.fert_P}
used_fertilizer_for_Potassium = {st.session_state.fert_K}
            """, language='python')

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### <span style='color: #E59A00;'>Step 3: Calculate Recommendations</span>", unsafe_allow_html=True)
        st.caption('Calculate the quantities of each fertilizer needed to meet the recommended N-P-K.')
        
        run = st.button('🎯 Calculate Now', use_container_width=True)
        
        if run:
            recom = FertilizerUsed().custom_fert(N=st.session_state.recom_amount['N'], P=st.session_state.recom_amount['P'], K=st.session_state.recom_amount['K'])

            fert_N = FertilizerUsed().custom_fert(N=st.session_state.fert_N['N'], P=st.session_state.fert_N['P'], K=st.session_state.fert_N['K'])
            fert_P = FertilizerUsed().custom_fert(N=st.session_state.fert_P['N'], P=st.session_state.fert_P['P'], K=st.session_state.fert_P['K'])
            fert_K = FertilizerUsed().custom_fert(N=st.session_state.fert_K['N'], P=st.session_state.fert_K['P'], K=st.session_state.fert_K['K'])

            result = FertilizerRecommendation(fertilizer_required=recom, area=st.session_state.recom_amount['area'])
            recoms = result.requirement(fert_N=fert_N, fert_P=fert_P, fert_K=fert_K)

            st.markdown(f"#### Results for **{st.session_state.recom_amount['area']} ha** area:")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric(
                    label=f"🟢 Nitrogen Fertilizer ({st.session_state.fert_N['N']}-{st.session_state.fert_N['P']}-{st.session_state.fert_N['K']})", 
                    value=f"{round(recoms['N']/50, 2)} bags", 
                    delta=f"{round(recoms['N'], 2)} kg", delta_color="off",
                )
            with c2:
                st.metric(
                    label=f"🔴 Phosphorus Fertilizer ({st.session_state.fert_P['N']}-{st.session_state.fert_P['P']}-{st.session_state.fert_P['K']})", 
                    value=f"{round(recoms['P']/50, 2)} bags", 
                    delta=f"{round(recoms['P'], 2)} kg", delta_color="off"
                )
            with c3:
                st.metric(
                    label=f"🔵 Potassium Fertilizer ({st.session_state.fert_K['N']}-{st.session_state.fert_K['P']}-{st.session_state.fert_K['K']})", 
                    value=f"{round(recoms['K']/50, 2)} bags", 
                    delta=f"{round(recoms['K'], 2)} kg", delta_color="off"
                )

            # Check for oversupply
            if 'oversupply' in recoms:
                oversupply = recoms['oversupply']
                oversupply_msg = []
                oversupply_recommendation = []
                if oversupply['N'] > 0:
                    oversupply_msg.append(f"Nitrogen (+{round(oversupply['N'], 2)} kg)")
                    oversupply_recommendation.append("Nitrogen")
                if oversupply['P'] > 0:
                    oversupply_msg.append(f"Phosphorus (+{round(oversupply['P'], 2)} kg)")
                    oversupply_recommendation.append("Phosphorus")
                if oversupply['K'] > 0:
                    oversupply_msg.append(f"Potassium (+{round(oversupply['K'], 2)} kg)")
                    oversupply_recommendation.append("Potassium")
                
                if oversupply_msg:
                    st.warning(f"**Potential oversupply detected:** {', '.join(oversupply_msg)}", icon="⚠️")
                    st.error(f"**Recommendation:** Consider changing the selected fertilizer grades for {', '.join(oversupply_recommendation)} to minimize nutrient oversupply.", icon="💡")