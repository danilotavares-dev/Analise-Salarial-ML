import streamlit as st
import json
import requests

# Título do app
st.title('💼 Modelo de Predição de Salário')

# Inputs do usuário
st.write('Quantos meses o profissional está na empresa?')
tempo_na_empresa = st.slider('Meses', min_value=1, max_value=120, value=60, step=1)

st.write('Qual o nível do profissional na empresa?')
nivel_na_empresa = st.slider('Nível', min_value=1, max_value=10, value=5, step=1)

input_features = {
    'tempo_na_empresa': tempo_na_empresa,
    'nivel_na_empresa': nivel_na_empresa
}

# Quando o botão for clicado
if st.button('Estimar Salário'):
    try:
        # Envia os dados para a API
        res = requests.post(
            url='http://127.0.0.1:8000/predict',
            json=input_features 
        )
        
        res.raise_for_status()
        res_json = res.json()
        st.write('🔍 Resposta do servidor:', res_json)
        chave_salario = 'salario em reais'

        if chave_salario in res_json:
            salario_em_reais = round(res_json[chave_salario], 2)
            st.subheader(f'💰 O salário estimado é de R$ {salario_em_reais}')
        else:
            st.error(f"A resposta não contém a chave '{chave_salario}'. "
                     f"Verifique o retorno do servidor acima.")

    except requests.exceptions.ConnectionError:
        st.error('❌ Não foi possível conectar ao servidor FastAPI. '
                 'Certifique-se de que ele está rodando em http://127.0.0.1:8000.')
        
    except Exception as e:
        st.error(f'⚠️ Ocorreu um erro: {e}')