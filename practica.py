import threading
import queue
import time
import random

# Simulación de un sistema de procesamiento de documentos con 4 trabajadores (hilos)
# Estudiante: Stephanie Lazarte
# Materia: Sistemas Operativos          Hito:4
trabajos = queue.Queue()
nombres = ["Vivi", "Arthur", "Mystery", "Lewis"]
resultados = {n: 0 for n in nombres}  # empiezan todos en 0 para que los 4 salgan en el resumen
detalle = []  # aquí guardo quién hizo cada documento
lock = threading.Lock()

# cargo los 24 documentos en la cola, cada uno con un tamaño al azar
for doc_id in range(1, 25):
    trabajos.put((doc_id, random.randint(1, 5)))


def trabajador(nombre):
    while True:
        try:
            # uso get_nowait y no empty() porque otro hilo podría sacar el último doc justo en medio
            doc_id, tamano = trabajos.get_nowait()
        except queue.Empty:
            break  # ya no quedan documentos, el trabajador termina

        time.sleep(tamano * 0.1)  # mientras más grande el doc, más se demora

        # el diccionario lo usan los 4 hilos, así que lo protejo con el lock
        with lock:
            resultados[nombre] += 1
            detalle.append((doc_id, tamano, nombre))
            print(f"{nombre} procesó el documento {doc_id} (tamaño {tamano})")


# creo y arranco los 4 hilos, uno por trabajador
hilos = []
for nombre in nombres:
    h = threading.Thread(target=trabajador, args=(nombre,))
    hilos.append(h)
    h.start()

# espero a que los 4 terminen antes de mostrar el resumen
for h in hilos:
    h.join()

print("\n--- RESUMEN ---")
print("Total procesado:", sum(resultados.values()))
for nombre in nombres:
    print(nombre, "->", resultados[nombre], "documentos")

# compruebo que ningún documento se haya repetido ni perdido
ids = [d[0] for d in detalle]
print("IDs únicos:", len(set(ids)), "de 24")