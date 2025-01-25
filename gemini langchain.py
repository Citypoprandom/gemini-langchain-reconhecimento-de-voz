
import os
import pyttsx3
import speech_recognition as sr
from langchain_google_genai import ChatGoogleGenerativeAI

# Define a chave da API do Google (lembre-se de não compartilhar chaves privadas publicamente)
os.environ["GOOGLE_API_KEY"] = "SUA_CHAVE_API"

# Inicializa o modelo Gemini
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

# Lista para armazenar o histórico da conversa
chat_history = [
    ("system", "Você é um assistente feito para ser um amigo fiel e companheiro, "
               "que não tenha frases muito longas e que faça conselhos ao Vitor (nome do cliente).",)
]

def main():
    assistente_falante = True
    ligar_microfone = True

    # Configura a voz do assistente
    if assistente_falante:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 180)  # Velocidade da voz

        print("\nLista de Vozes - Verifique o número\n")
        for indice, vozes in enumerate(voices):
            print(indice, vozes.name)

        voz = 0  # Escolha a voz que você quer usar
        engine.setProperty('voice', voices[voz].id)

    # Configura o microfone para reconhecimento de voz
    if ligar_microfone:
        r = sr.Recognizer()
        mic = sr.Microphone(2)

    bem_vindo = "# Bem Vindo ao assistente do Vitor #"
    print("\n" + len(bem_vindo) * "#")
    print(bem_vindo)
    print(len(bem_vindo) * "#")
    print("###   Diga 'desligar' para encerrar    ###")
    print("")

    while True:
        texto = ""
        response_text = ""  # Inicializa a variável para evitar erro de referência

        if ligar_microfone:
            with mic as fonte:
                r.adjust_for_ambient_noise(fonte)
                print("Fale alguma coisa (ou diga 'desligar')")
                audio = r.listen(fonte)
                print("Enviando para reconhecimento")
                try:
                    texto = r.recognize_google(audio, language="pt-BR")
                    print("Você disse: {}".format(texto))

                    # Adiciona entrada do usuário ao histórico
                    chat_history.append(("human", texto))

                    # Gera resposta usando o histórico da conversa
                    ai_msg = llm.invoke(chat_history)
                    response_text = ai_msg.content  # Acessa o conteúdo gerado pelo modelo

                    # Adiciona resposta da IA ao histórico
                    chat_history.append(("ai", response_text))

                except Exception as e:
                    print("Não entendi o que você disse. Erro:", e)
                    response_text = "Desculpe, não entendi. Pode repetir?"

        else:

            # Adiciona entrada do usuário ao histórico
            chat_history.append(("human", texto))

            # Gera resposta usando o histórico da conversa
            ai_msg = llm.invoke(chat_history)
            response_text = ai_msg.content  # Acessa o conteúdo gerado pelo modelo

            # Adiciona resposta da IA ao histórico
            chat_history.append(("ai", response_text))

        print("Gemini:", response_text, "\n")

        if assistente_falante:
            engine.say(response_text)
            engine.runAndWait()

    print("Encerrando Chat")

if __name__ == '__main__':
    main()
