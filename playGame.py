import time
import keyboard

# Tempo total de execução do loop (40 segundos)
tempo_total = 40

# Tempo de espera entre cada pressionamento de tecla (5 segundos)
tempo_espera = 0.5

# Tempo decorrido
tempo_decorrido = 0

# Flag para controlar o loop
executando = True

time.sleep(5)

try:
    while tempo_decorrido < tempo_total:
        # Pressiona a tecla espaço

        for i in range(3):
            keyboard.press_and_release('space')
            time.sleep(0.2)

        # Incrementa o tempo decorrido
        tempo_decorrido += tempo_espera

        # Espera 5 segundos antes de repetir o loop
        time.sleep(tempo_espera)

        # Pressiona a tecla Enter
        keyboard.press_and_release('enter')
except KeyboardInterrupt:
    # Encerrar o loop se o usuário pressionar Ctrl+C
    executando = False

if executando:
    print("Loop encerrado após 40 segundos.")
else:
    print("Loop interrompido pelo usuário.")