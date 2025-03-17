import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.font_manager as fm

# 🔹 โหลดฟอนต์ภาษาไทย
font_path = "C:/Windows/Fonts/THSarabunNew.ttf"  # ตรวจสอบว่าไฟล์ฟอนต์มีอยู่จริง
font_prop = fm.FontProperties(fname=font_path)

# 🔹 ตั้งค่าชื่อแอป
st.title("📊 คำนวณเงินบำนาญจากเงินเดือน")

# 🔹 รับค่าอายุตัว
old_year = st.number_input("อายุ (ปี)", max_value=60, value=15, step=1)
# 🔹 รับค่าอายุราชการ
work_year = st.number_input("อายุราชการ (ปี)", min_value=0, value=25, step=1)

# 🔹 รับค่าเงินเดือนย้อนหลัง 8 ครั้ง (4 ปี) -> 1 ปีเพิ่มเงินเดือน 2 ครั้ง
st.subheader("📌 กรอกเงินเดือนย้อนหลัง 8 ครั้ง (4 ปี)")
cols = st.columns(8)  # แบ่งเป็น 8 คอลัมน์
salaries = []
for i in range(8):
    with cols[i]:  
        salary = st.number_input(f"เลื่อนเงินเดือนย้อนหลัง {i+1}", min_value=0, value=30000, step=1000, key=f"salary_{i}")
        salaries.append(salary)

# 🔹 คำนวณเงินบำนาญ
salary_avg = sum(salaries) / len(salaries)  # ค่าเฉลี่ยเงินเดือนย้อนหลัง 8 ครั้ง
pension = salary_avg * work_year / 50  # คำนวณเงินบำนาญ
pension = min(pension, salary_avg * 0.7)  # จำกัดไม่เกิน 70% ของเงินเดือนเฉลี่ย

# 🔹 แสดงผลลัพธ์
st.subheader("💰 ผลการคำนวณเงินบำนาญ")
st.write(f"🔹 **เงินเดือนเฉลี่ยย้อนหลัง:** {salary_avg:,.2f} บาท")
st.write(f"🔹 **เงินบำนาญต่อเดือน (จากเงินเดือนเฉลี่ย):** {pension:,.2f} บาท")

# 🔹 ทำนายเงินเดือนในอนาคต (เพิ่มขึ้นครั้งละ 2.25% ทุกครึ่งปี)
st.subheader("📈 ทำนายเงินเดือนเฉลี่ยในอนาคต")
future_years = min(60-old_year, old_year)  # จำกัดให้แสดงผลอายุตัวไม่เกิน 60 ปี
predicted_salaries = [salaries[-1]]  # เริ่มจากเงินเดือนล่าสุดที่ผู้ใช้กรอก

for _ in range(future_years * 2):  # *2 เพราะเลื่อนเงินเดือนปีละ 2 ครั้ง
    next_salary = predicted_salaries[-1] * 1.0225  # เพิ่ม 2.25% ทุกครั้ง
    predicted_salaries.append(next_salary)

# 🔹 คำนวณเงินบำนาญทำนายจากเงินเดือนที่เพิ่มขึ้น
predicted_pensions = []
for salary in predicted_salaries:
    predicted_pension = salary * work_year / 50  # คำนวณเงินบำนาญจากเงินเดือนทำนาย
    predicted_pension = min(predicted_pension, salary * 0.7)  # จำกัดไม่เกิน 70% ของเงินเดือนทำนาย
    predicted_pensions.append(predicted_pension)

# 🔹 สร้างกราฟแสดงเงินเดือนทำนายและเงินบำนาญทำนาย (ใช้ plotly)
fig = go.Figure()

# กราฟเงินเดือนทำนาย
fig.add_trace(go.Scatter(
    x=np.arange(work_year, work_year + len(predicted_salaries) / 2, 0.5),
    y=predicted_salaries,
    mode='lines+markers',
    name='เงินเดือนเฉลี่ยทำนาย',
    marker=dict(color='blue'),
    hovertemplate="ปี: %{x}<br>เงินเดือนเฉลี่ย: %{y:,.2f} บาท"
))

# กราฟเงินบำนาญทำนาย
fig.add_trace(go.Scatter(
    x=np.arange(work_year, work_year + len(predicted_salaries) / 2, 0.5),
    y=predicted_pensions,
    mode='lines+markers',
    name='เงินบำนาญทำนาย',
    marker=dict(color='red'),
    hovertemplate="ปี: %{x}<br>เงินบำนาญ: %{y:,.2f} บาท"
))

# ปรับแต่งกราฟ
fig.update_layout(
    title="📊 การทำนายเงินเดือนเฉลี่ยและเงินบำนาญในอนาคต",
    xaxis_title="ปีที่รับราชการ",
    yaxis_title="จำนวนเงิน (บาท)",
    template="plotly_dark",
    showlegend=True
)

# แสดงกราฟ
st.plotly_chart(fig)
