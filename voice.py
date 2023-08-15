import speech_recognition as sr
import pyttsx3
from deepmultilingualpunctuation import PunctuationModel

# Inicializa o modelo de pontuação
model = PunctuationModel(model="kredor/punctuate-all")

# Função para falar o texto
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Inicializa o recognizer
r = sr.Recognizer()

# Avisa o usuário que a gravação vai começar
print("Por favor, comece a falar em 3 segundos.")
print("3")
print("2")
print("1")

# Configuração do microfone
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Gravando...")
    audio = r.listen(source)

    # Reconhecimento de voz
    try:
        MyText = r.recognize_google(audio, language="pt-BR")
        print("Você disse: " + MyText)

        # Formata o texto em minúsculas e remove a pontuação
        MyText = MyText.lower().replace(",", "").replace(".", "").replace("?", "").replace("!", "")
        print("Texto formatado: " + MyText)

        # Adiciona a pontuação de volta
        MyText = model.restore_punctuation(MyText)
        print("Texto pontuado: " + MyText)

        # Fala o texto
        print(MyText)

    except sr.UnknownValueError:
        print("Não foi possível entender o que você disse")
    except sr.RequestError as e:
        print("Não foi possível se conectar ao serviço de reconhecimento de voz; {0}".format(e))
