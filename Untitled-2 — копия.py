import speech_recognition as sr 


r = sr.Recognizer()
with sr.Microphone(device_index=1) as source:
    print("кажите что-нибудь ...")
    audio = r.listen(source)
query = r.recognize_google(audio, Language="ru-RU")
print("Вы сказали: "+ query.lower())