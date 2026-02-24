import streamlit as st
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title="HIS جهادی ابری", layout="wide")

# اتصال به دیتابیس ابری (اطلاعات حساس در تنظیمات مخفی می‌ماند)
conn = st.connection("supabase", type=SupabaseConnection)

st.title("🏥 سامانه یکپارچه سلامت (HIS کوچک)")

# ایجاد تب برای نظم بیشتر
tab1, tab2 = st.tabs(["ثبت بیمار جدید", "مشاهده پرونده‌ها"])

with tab1:
    with st.form("patient_form"):
        col1, col2 = st.columns(2)
        with col1:
            id_card = st.text_input("کد ملی")
            name = st.text_input("نام بیمار")
        with col2:
            age = st.number_input("سن", 0, 120)
            
        symptoms = st.text_area("شرح حال و علائم")
        prescription = st.text_area("تجویز و دارو")
        
        if st.form_submit_button("ذخیره در سرور ابری"):
            # ارسال داده به دیتابیس آنلاین
            data = conn.table("patients").insert([
                {"national_id": id_card, "full_name": name, "age": age, "symptoms": symptoms, "prescription": prescription}
            ]).execute()
            st.success("اطلاعات با موفقیت در سرور ابری ذخیره شد.")

with tab2:
    st.subheader("جستجو و لیست بیماران")
    search_query = st.text_input("جستجوی نام یا کد ملی")
    
    # دریافت اطلاعات از سرور
    rows = conn.table("patients").select("*").execute()
    df = pd.DataFrame(rows.data)
    
    if not df.empty:
        if search_query:
            df = df[df['full_name'].str.contains(search_query) | df['national_id'].str.contains(search_query)]
        st.dataframe(df)