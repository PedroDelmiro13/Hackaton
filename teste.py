import openai
from transformers import pipeline
from collections import Counter

openai.api_key = "sk-proj-czN45unVprFrBFtB28QHRBJ0bDr8fmgiXEaXygsuwMBlojjx31OhpEMG-oCRpMhLdsj2SUQecaT3BlbkFJuU-1jMcVjXL-"
mensagem = "assalto" #usar algo que linke a mensagem pra ca
classifier = pipeline("zero-shot-classification") #isso é da transformers, pra organizar sendo algo q eles nao reconhecem

def verificar_linguagem_natural(mensagem):
    prompt = f"Verifique se essa mensagem possui uma linguagem natural. Responda apenas com 'Sim' ou 'Não' '{mensagem}'"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.2
    )
    resposta =  response.choices[0].message['content'].strip().lower()
    if resposta == 'Sim':
        return True
    elif resposta == 'Não':
        return False
    else:
        return False
def classificar_mensagem(mensagem):
    result = classifier(mensagem, candidate_labels=["assalto", "noticia"])
    return result['labels'][0]

def verificar_deepfake(mensagem):
    #ainda nao fiz nada com deepfake, nao sei como usar
    #mas seria algo do tipo
    if "deepfake" in mensagem.lower(): #pra pegar tudo
        return True
    return False
def remover_conteudo_indevido(mensagem):
    spam = ["sexo"]
    palavras = mensagem.lower().split()
    for palavra in spam:
        if palavra in palavras:
            palavras.remove(palavra)
    return mensagem
def definir_urgencia(mensagem):
    key_words = ["assalto", "roubo"]
    palavras = mensagem.lower().split()
    contagem = Counter(palavra for palavra in palavras if palavra in key_words)
    return contagem
def classificar_urgencia(mensagem):
    urgencia = definir_urgencia(mensagem)
    total_key_words = sum(urgencia.values())
    
    if sum(total_key_words) >= 3:
        return "Muito alta"
    elif sum(total_key_words) == 2:
        return "Alta"
    elif sum(total_key_words) == 1:
        return "Padrão"
    elif sum(total_key_words) == 0:
        return "Pouco"
    else:
        return "Sem gravidade"
    
def mensagem_processada(mensagem):
    if not verificar_linguagem_natural(mensagem):
        print("sem linguagem natural")
        return
    is_deepfake = verificar_deepfake(mensagem)
    if is_deepfake:
        print("deepfake identificada")
        return
    
    mensagem = remover_conteudo_indevido(mensagem)
    categoria = classificar_mensagem(mensagem)
    urgencia = classificar_urgencia(mensagem)

    print(f"Categoria: {categoria}")
    print(f"É deepfake? {'Sim' if is_deepfake else 'Não'}")
    print(f"Urgência e palavras-chave: {urgencia}")

mensagem_processada(mensagem)