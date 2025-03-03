


import streamlit as st
import pandas as pd
import sqlite3

# Criar conexão com o banco de dados SQLite3
conn = sqlite3.connect("dados_imc.db", check_same_thread=False)
cursor = conn.cursor()

# Criar tabela caso não exista
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        peso REAL,
        altura REAL,
        idade INTEGER,
        sexo TEXT,
        imc REAL,
        massa_corporal REAL,
        gordura_corporal REAL,
        classificacao TEXT,
        grau TEXT
    )
''')
conn.commit()

# Função para calcular o IMC
def calcular_imc(peso, altura):
    return peso / (altura ** 2)

# Função para calcular a massa corporal
def calcular_massa_corporal(peso):
    return peso

# Função para calcular a porcentagem de gordura corporal (estimativa simplificada)
def calcular_gordura_corporal(imc, idade, sexo):
    if sexo.lower() == 'masculino':
        gordura_corporal = (1.20 * imc) + (0.23 * idade) - 16.2
    else:
        gordura_corporal = (1.20 * imc) + (0.23 * idade) - 5.4
    return gordura_corporal

# Função para classificar o grau de IMC
def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso", None
    elif 18.5 <= imc < 24.9:
        return "Peso normal", None
    elif 25 <= imc < 29.9:
        return "Sobrepeso", None
    elif 30 <= imc < 34.9:
        return "Obesidade", "Grau 1"
    elif 35 <= imc < 39.9:
        return "Obesidade", "Grau 2"
    else:
        return "Obesidade", "Grau 3"

# Interface gráfica com Streamlit
st.write("acompanhe o seu desempenho.")
st.title("Calculadora de IMC - Fitness")

peso = st.number_input("Digite seu peso (kg):", min_value=1.0, format="%.2f")
altura = st.number_input("Digite sua altura (m):", min_value=0.5, format="%.2f")
idade = st.number_input("Digite sua idade:", min_value=1, step=1)
sexo = st.radio("Digite seu sexo:", ["Masculino", "Feminino"])

if st.button("Calcular IMC"):
    if peso > 0 and altura > 0:
        imc = calcular_imc(peso, altura)
        massa_corporal = calcular_massa_corporal(peso)
        gordura_corporal = calcular_gordura_corporal(imc, idade, sexo)
        classificacao, grau = classificar_imc(imc)
        
        # Exibir resultados
        st.write(f"*IMC:* {imc:.2f}")
        st.write(f"*Massa Corporal:* {massa_corporal} kg")
        st.write(f"*Porcentagem de Gordura Corporal:* {gordura_corporal:.2f}%")
        st.write(f"*Classificação do IMC:* {classificacao}")
        if grau:
            st.write(f"*Grau de obesidade:* {grau}")

        # Salvar no banco de dados
        cursor.execute('''
            INSERT INTO usuarios (peso, altura, idade, sexo, imc, massa_corporal, gordura_corporal, classificacao, grau)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (peso, altura, idade, sexo, imc, massa_corporal, gordura_corporal, classificacao, grau))
        conn.commit()

# Exibir histórico de registros salvos
st.subheader("Histórico de usuários cadastrados")
df = pd.read_sql_query("SELECT * FROM usuarios", conn)
st.dataframe(df)

# Opção para excluir o histórico
st.subheader("Excluir histórico de registros")
senha = st.text_input("Digite a senha para limpar o histórico:", type="password")

if st.button("Excluir histórico"):
    if senha == "1235":
        cursor.execute("DELETE FROM usuarios")
        conn.commit()
        st.success("Histórico apagado com sucesso!")
    else:
        st.error("Senha incorreta. Tente novamente.")

# Fechar conexão
conn.close()