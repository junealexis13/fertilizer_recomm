import streamlit as st
from fertilizer_recom import FertilizerRecommendation, FertilizerUsed

def app():
    st.markdown('#### *Step 1: Recommended Ammounts (N-P-K)*')
    st.caption('Enter the recommended amounts of N, P, and K for the crop')

    with st.container(border=True, horizontal=False):
        with st.container(horizontal=True, horizontal_alignment='left', width='stretch'):
            recom_N = st.number_input("Recommended N", min_value=0, max_value=100, value=50, width='stretch', key="recom_N")
            recom_P = st.number_input("Recommended P", min_value=0, max_value=100, value=50, width='stretch', key="recom_P")
            recom_K = st.number_input("Recommended K", min_value=0, max_value=100, value=50, width='stretch', key="recom_K")
        with st.container(horizontal=True, horizontal_alignment='left', width='content'):
            area = st.text_input("Area (ha)", value=1, width='stretch', key="area")
    st.session_state.recom_amount = {'N': recom_N, 'P': recom_P, 'K': recom_K, 'area': float(area)}

    if st.session_state.recom_amount['N'] > 0 or st.session_state.recom_amount['P'] > 0 or st.session_state.recom_amount['K'] > 0:
        st.markdown('#### *Step 2: Update Fertilizer Amounts*')
        st.caption('Update fertilizer information to be calculated to fulfill the recommended amounts. ')
        st.text('Go to the sidebar to update.')

        st.code(f"""
            # recommended amounts
            recom_amount = {st.session_state.recom_amount}

            # used fertilizers to fulfill the recommended amounts
            used_fertilizer_for_Nitrogen = {st.session_state.fert_N}
            used_fertilizer_for_Potassium = {st.session_state.fert_P}
            used_fertilizer_for_Potassium = {st.session_state.fert_K}
        """, language='python')

    with st.container(border=True):
        st.markdown('#### *Step 3: Calculate Fertilizer Amounts*')
        st.caption('Calculate the amounts of each fertilizer needed to fulfill the recommended amounts.')
        
        run = st.button('Calculate')
        if run:
            recom = FertilizerUsed().custom_fert(N=st.session_state.recom_amount['N'], P=st.session_state.recom_amount['P'], K=st.session_state.recom_amount['K'])

            fert_N = FertilizerUsed().custom_fert(N=st.session_state.fert_N['N'], P=st.session_state.fert_N['P'], K=st.session_state.fert_N['K'])
            fert_P = FertilizerUsed().custom_fert(N=st.session_state.fert_P['N'], P=st.session_state.fert_P['P'], K=st.session_state.fert_P['K'])
            fert_K = FertilizerUsed().custom_fert(N=st.session_state.fert_K['N'], P=st.session_state.fert_K['P'], K=st.session_state.fert_K['K'])

            result = FertilizerRecommendation(fertilizer_required=recom, area=st.session_state.recom_amount['area'])
            recoms = result.requirement(fert_N=fert_N, fert_P=fert_P, fert_K=fert_K)

            with st.container(border=True):
                st.markdown('### Fertilizer Recommendation')
                st.write(f'For :blue[{st.session_state.recom_amount['area']} ha], you need to apply:')
            
                with st.container():
                    st.markdown('#### Nitrogen')
                    st.write(f'You need to apply :green[{round(recoms['N'], 2)} kg], or :blue[{round(recoms['N']/50, 2)} bag/s] of :orange[{st.session_state.fert_N['N']}-{st.session_state.fert_N['P']}-{st.session_state.fert_N['K']}]')
                with st.container():
                    st.markdown('#### Phosphorus')
                    st.write(f'You need to apply :green[{round(recoms['P'], 2)} kg], or :blue[{round(recoms['P']/50, 2)} bag/s] of :orange[{st.session_state.fert_P['N']}-{st.session_state.fert_P['P']}-{st.session_state.fert_P['K']}]')
                with st.container():
                    st.markdown('#### Potassium')
                    st.write(f'You need to apply :green[{round(recoms['K'], 2)} kg], or :blue[{round(recoms['K']/50, 2)} bag/s] of :orange[{st.session_state.fert_K['N']}-{st.session_state.fert_K['P']}-{st.session_state.fert_K['K']}]')