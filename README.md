# 🏅 Olympics Data Analysis Web App

### Overview
An interactive **Streamlit web application** that explores over a century of Olympic Games data (1896–2016).  
It provides insightful visualizations of **medal tallies, athlete performance, country-wise progress,** and **gender participation trends** — all in one intuitive dashboard.

🔗 **Live App:** [Olympics Analysis Web App](https://olympicsanalysis-webapp.streamlit.app/)  

---

## 🧩 Features

✅ Dynamic medal tally with gradient highlighting  
✅ Interactive filters (Year, Country, Sport, and Event)  
✅ Athlete age and performance analysis  
✅ Country-wise medal progression charts  
✅ Gender participation comparison  
✅ Height vs. Weight scatter visualization  
✅ Fully dark-themed modern UI  

---

## 💡 Insights

- Participation has grown from **14 nations in 1896** to **over 200 in 2016**  
- **Women’s participation** has increased significantly since the **1980s**  
- Different sports exhibit unique **age and physical characteristics** among athletes  
- The **USA** and **Soviet Union** dominate historical medal standings  

---

## 🛠️ Tech Stack

| Category | Tools |
|-----------|-------|
| **Language** | Python |
| **Framework** | Streamlit |
| **Libraries** | Pandas, Numpy, Matplotlib, Seaborn, Plotly |
| **Data Source** | Kaggle – Olympics Dataset |
| **Version Control** | Git & GitHub |

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/komal-sukheja/Olympics_Analysis_web_app.git
cd Olympics_Analysis_web_app

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # For Windows
# OR
source venv/bin/activate   # For Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
