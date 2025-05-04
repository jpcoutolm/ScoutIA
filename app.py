
import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

st.set_page_config(page_title="Scout IA - Futebol Amador", layout="wide")
st.markdown(
    """
    <style>
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem !important;
            }
            h1 {
                font-size: 1.5rem !important;
            }
        }
        .css-1d391kg {
            padding: 1rem !important;
        }
    </style>
    """, unsafe_allow_html=True
)

st.title("⚽ Scout IA - Análise Inteligente de Partidas Amadoras")

st.markdown("Preencha os dados da partida para gerar estatísticas, gráficos e um relatório completo em PDF.")

with st.expander("➕ Adicionar jogadores"):
    num_jogadores = st.number_input("Quantos jogadores deseja registrar?", min_value=1, max_value=20, value=5)
    dados = []

    for i in range(int(num_jogadores)):
        with st.container():
            st.markdown(f"**Jogador {i+1}**")
            cols = st.columns(2)
            nome = cols[0].text_input("Nome", key=f"nome_{i}")
            gols = cols[1].number_input("Gols", min_value=0, key=f"gols_{i}")
            passes_certos = cols[0].number_input("Passes certos", min_value=0, key=f"pc_{i}")
            passes_errados = cols[1].number_input("Passes errados", min_value=0, key=f"pe_{i}")
            finalizacoes = cols[0].number_input("Finalizações", min_value=0, key=f"fin_{i}")
            faltas = cols[1].number_input("Faltas cometidas", min_value=0, key=f"faltas_{i}")
            minutos = cols[0].number_input("Minutos jogados", min_value=0, key=f"min_{i}")

            dados.append({
                "Nome": nome,
                "Gols": gols,
                "Passes Certos": passes_certos,
                "Passes Errados": passes_errados,
                "Finalizações": finalizacoes,
                "Faltas": faltas,
                "Minutos Jogados": minutos
            })

if st.button("📊 Gerar Scout"):
    df = pd.DataFrame(dados)
    df["Eficiência de Passe (%)"] = round(df["Passes Certos"] / (df["Passes Certos"] + df["Passes Errados"]) * 100, 1)
    df["Impacto Ofensivo"] = df["Gols"] * 2 + df["Finalizações"]

    st.subheader("📈 Resultados da Partida")
    st.dataframe(df.sort_values(by="Impacto Ofensivo", ascending=False), use_container_width=True)

    fig = px.bar(df, x="Nome", y="Impacto Ofensivo", title="Impacto Ofensivo por Jogador", text="Impacto Ofensivo")
    st.plotly_chart(fig, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar CSV", data=csv, file_name="scout_partida.csv", mime="text/csv")

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "Relatório de Scout - Partida", ln=True, align="C")
            self.ln(10)
        def jogador_info(self, jogador):
            self.set_font("Arial", "", 12)
            for key, value in jogador.items():
                self.cell(0, 8, f"{key}: {value}", ln=True)
            self.ln(5)

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    for _, row in df.iterrows():
        pdf.jogador_info(row.to_dict())
    pdf.output("relatorio_scout.pdf")
    with open("relatorio_scout.pdf", "rb") as file:
        st.download_button("📄 Baixar PDF", data=file, file_name="relatorio_scout.pdf")
