
import streamlit as st
import pandas as pd

# ========================
# Carregamento da Tabela Nutricional
# ========================
@st.cache_data
def carregar_tabela_nutricional():
    return pd.read_csv("tabela_valores_nutricionais_com_acucar_lactose.csv")

df_nutri = carregar_tabela_nutricional()

# ========================
# Registro de Alimentos
# ========================
st.title("📊 Registro de Consumo Alimentar")

# Input do alimento
alimento = st.selectbox("Selecione o alimento consumido:", df_nutri["Alimento"].unique())
quantidade = st.number_input("Quantidade consumida (em gramas ou ml):", min_value=0.0, step=1.0)

if st.button("Registrar Consumo"):
    info = df_nutri[df_nutri["Alimento"] == alimento].iloc[0]
    fator = quantidade / 100  # pois os valores são por 100g/ml

    calorias = round(info["Calorias (kcal)"] * fator, 2)
    carboidratos = round(info["Carboidratos (g)"] * fator, 2)
    acucar = round(info["Açúcar (g)"] * fator, 2)
    lactose = info["Lactose"]

    novo_registro = {
        "Alimento": alimento,
        "Quantidade (g/ml)": quantidade,
        "Calorias": calorias,
        "Carboidratos": carboidratos,
        "Açúcar": acucar,
        "Lactose": lactose
    }

    if "registro" not in st.session_state:
        st.session_state["registro"] = []

    st.session_state["registro"].append(novo_registro)
    st.success("Alimento registrado com sucesso!")

    if lactose == "Sim":
        st.warning("⚠️ Atenção: este alimento contém lactose.")

# ========================
# Exibir Registros
# ========================
if "registro" in st.session_state and st.session_state["registro"]:
    df_registro = pd.DataFrame(st.session_state["registro"])
    st.subheader("📋 Registro do Dia")
    st.dataframe(df_registro, use_container_width=True)

    st.subheader("🔢 Totais do Dia")
    total = df_registro[["Calorias", "Carboidratos", "Açúcar"]].sum()
    st.write(f"**Total de Calorias:** {total['Calorias']} kcal")
    st.write(f"**Total de Carboidratos:** {total['Carboidratos']} g")
    st.write(f"**Total de Açúcar:** {total['Açúcar']} g")
else:
    st.info("Nenhum alimento registrado ainda.")
