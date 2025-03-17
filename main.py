import streamlit as st


st.title("hello")
# ข้อความต้อนรับที่กำหนดเอง
st.markdown("""
    # ยินดีต้อนรับสู่แอปของเรา!
    หากคุณต้องการข้อมูลเพิ่มเติม, โปรดติดต่อเราทางอีเมล
""")
# ฟังก์ชันที่ใช้แสดงผลลัพธ์เมื่อมีการเปลี่ยนแปลง
def show_greeting():
    name = st.session_state.name
    if name:
        st.write(f"สวัสดี {name}จร้า")
    else:
        st.write("ยังไม่ได้กรอกชื่อ")

# สร้าง text input พร้อมกับการตั้งค่า on_change
st.text_input("กรุณากรอกชื่อของคุณ:", key="name", on_change=show_greeting)