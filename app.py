import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd  # اضافه شد

st.set_page_config(page_title="HIS جهادی ابری", layout="wide")

# اتصال به دیتابیس ابری
# روش مستقیم برای اطمینان از اتصال
tmp_url = "https://vufsmlyybxqyphgozofx.supabase.co"
tmp_key = "sb_publishable_VqFoEVlp3rLWzwV7Nq6Acg_rXBZS13UuJvG-z_8-2W1"
conn = st.connection("supabase", type=SupabaseConnection, url=tmp_url, key=tmp_key)

st.title("🏥 سامانه یکپارچه سلامت (HIS کوچک)")

# ایجاد تب برای نظم بیشتر
tab1, tab2 = st.tabs(["ثبت بیمار جدید", "مشاهده پرونده‌ها"])

with tab1:
    with st.form("patient_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            id_card = st.text_input("کد ملی")
            name = st.text_input("نام بیمار")
        with col2:
            age = st.number_input("سن", 0, 120)
            
        symptoms = st.text_area("شرح حال و علائم")
        prescription = st.text_area("تجویز و دارو")
        
        if st.form_submit_button("ذخیره در سرور ابری"):
            if id_card and name:
                try:
                    res = conn.table("patients").insert([
                        {"national_id": id_card, "full_name": name, "age": age, "symptoms": symptoms, "prescription": prescription}
                    ]).execute()
                    st.success(f"اطلاعات {name} با موفقیت ذخیره شد.")
                except Exception as e:
                    st.error(f"خطای دیتابیس: {e}") # این خط علت واقعی را به شما می‌گوید
            else:
                st.warning("لطفاً کد ملی و نام بیمار را وارد کنید.")

with tab2:
    st.subheader("جستجو و لیست بیماران")
    
    # دریافت اطلاعات از سرور
    try:
        response = conn.table("patients").select("*").execute()
        # استخراج داده‌ها
        data = response.data
        
        if data:
            df = pd.DataFrame(data)
            
            # بخش جستجو
            search_query = st.text_input("جستجوی نام یا کد ملی")
            if search_query:
                # فیلتر کردن دیتافریم بر اساس جستجو
                df = df[df['full_name'].astype(str).str.contains(search_query) | 
                        df['national_id'].astype(str).str.contains(search_query)]
            
            # نمایش جدول
            st.dataframe(df, use_container_width=True)
            
            # دکمه رفرش
            if st.button("به‌روزرسانی لیست"):
                st.rerun()
        else:
            st.info("هنوز هیچ بیماری در سیستم ثبت نشده است.")
            
    except Exception as e:
        st.error(f"خطا در دریافت اطلاعات: {e}")


