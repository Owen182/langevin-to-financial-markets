# Langevin to Financial Markets

โครงสำหรับ Quant research project ที่ศึกษาการประยุกต์ Langevin dynamics กับตลาดการเงิน
โดยตั้งใจเว้น implementation ไว้ให้ลงมือพัฒนาและทดลองด้วยตัวเอง

## Project structure

```text
langevin-to-financial-markets/
├── configs/                 # ค่าตั้งต้นของ experiment แต่ละชุด
├── data/
│   ├── raw/                 # ข้อมูลต้นฉบับ ห้ามแก้ทับ
│   ├── external/            # ข้อมูลจากแหล่งอื่น เช่น risk-free rate
│   ├── interim/             # ข้อมูลระหว่างการ clean/transform
│   └── processed/           # ชุดข้อมูลพร้อมใช้กับ model
├── docs/                    # สมมติฐาน นิยาม และบันทึกการตัดสินใจ
├── notebooks/               # EDA และลำดับการทดลอง
├── reports/
│   ├── figures/             # กราฟสำหรับรายงาน
│   └── tables/              # ตารางผลลัพธ์
├── scripts/                 # คำสั่งรัน pipeline/experiment
├── src/langevin_finance/
│   ├── data/                # โหลดและตรวจคุณภาพข้อมูล
│   ├── features/            # returns, volatility, state variables
│   ├── models/              # Langevin/SDE และ calibration
│   ├── evaluation/          # diagnostics, metrics, backtest
│   └── visualization/       # plotting functions
├── tests/                   # tests ของโค้ดใน src/
├── outputs/                 # ผลรันชั่วคราว ไม่ commit
├── .env.example             # ตัวอย่าง environment variables/API keys
├── .gitignore
└── requirements.txt         # dependencies ที่คุณเลือกใช้
```

## ลำดับที่แนะนำให้ทำ

1. เขียน research question และนิยาม state variable ใน `docs/research-plan.md`
2. เลือกสินทรัพย์ ความถี่ข้อมูล และช่วงเวลา
3. ทำ EDA ใน `notebooks/01_data_eda.ipynb`
4. สร้าง Langevin/OU baseline ด้วยตัวเองใน `src/langevin_finance/models/`
5. ทำ parameter estimation และ residual diagnostics
6. แบ่ง train/validation/test ตามเวลา และทำ walk-forward test
7. เปรียบเทียบกับ baseline ที่ง่ายกว่า
8. เพิ่ม transaction costs และตรวจ look-ahead/survivorship bias ก่อนสรุปผล

## Notebook naming

```text
01_data_eda.ipynb
02_state_variable.ipynb
03_langevin_baseline.ipynb
04_calibration_diagnostics.ipynb
05_simulation_validation.ipynb
06_strategy_backtest.ipynb
```

เริ่มจาก model เล็กที่สุดก่อน และย้ายเฉพาะโค้ดที่ใช้ซ้ำออกจาก notebook ไปไว้ใน `src/`.

