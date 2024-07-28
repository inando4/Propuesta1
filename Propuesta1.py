import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.optimize import fsolve
import tkinter as tk
from tkinter import ttk

# Parámetros iniciales
b = 0.22  # Rozamiento
v0 = 60   # Velocidad de disparo
u = v0 / 2  # Velocidad del viento
alfa = np.pi  # Dirección
h0 = 10  # Altura inicial

# Funciones f_x y f_y
def f_x(t, angulo, b, v0, u, alfa):
    return u * np.cos(alfa) * t + (v0 * np.cos(angulo) - u * np.cos(alfa)) * (1 - np.exp(-b * t)) / b

def f_y(t, angulo, b, v0, u, alfa, h0):
    return h0 + (9.8 / b + v0 * np.sin(angulo) - u * np.sin(alfa)) * (1 - np.exp(-b * t)) / b - (9.8 / b - u * np.sin(alfa)) * t

# Función para actualizar la animación
def update_animation(b, v0, u, alfa, h0, angulo_deg):
    angulo = np.radians(angulo_deg)
    T0 = 2 * v0 * np.sin(angulo) / 9.8  # Tiempo de vuelo sin rozamiento
    t_vuelo = fsolve(lambda t: f_y(t, angulo, b, v0, u, alfa, h0), T0)[0]  # Tiempo de vuelo
    tt = np.linspace(0, t_vuelo, 100)
    x1 = f_x(tt, angulo, b, v0, u, alfa)
    y1 = f_y(tt, angulo, b, v0, u, alfa, h0)

    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.75)  # Ajustar el espacio para el texto

    ax.set_xlim(0, 350)  # Límite fijo para el eje x
    ax.set_ylim(0, 100)  # Límite fijo para el eje y
    ax.grid(True)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title('Tiro parabólico con rozamiento y viento')

    line, = ax.plot([], [], '-', lw=2)
    text = ax.text(1.05, 0.5, '', transform=ax.transAxes, fontsize=12, verticalalignment='center')

    def animate(i):
        line.set_data(x1[:i+1], y1[:i+1])
        text.set_text(f'Tiempo: {tt[i]:.2f} s\nx: {x1[i]:.2f} m\ny: {y1[i]:.2f} m')
        return line, text

    ani = animation.FuncAnimation(fig, animate, frames=len(tt), interval=50)
    plt.show()

# Función para obtener los valores de los sliders y actualizar la animación
def get_values_and_update():
    b = float(b_entry.get())
    v0 = float(v0_entry.get())
    u = float(u_entry.get())
    alfa = np.radians(float(alfa_entry.get()))
    h0 = float(h0_entry.get())
    angulo = float(angulo_entry.get())
    update_animation(b, v0, u, alfa, h0, angulo)

# Crear la ventana principal
root = tk.Tk()
root.title("Parámetros del Tiro Parabólico")

# Crear sliders y entradas para los parámetros
def create_slider_and_entry(label_text, from_, to, initial_value):
    frame = ttk.Frame(root)
    frame.pack()
    label = ttk.Label(frame, text=label_text)
    label.pack(side=tk.LEFT)
    slider = ttk.Scale(frame, from_=from_, to=to, orient='horizontal', length=200)
    slider.set(initial_value)
    slider.pack(side=tk.LEFT)
    entry = ttk.Entry(frame, width=10)
    entry.insert(0, str(initial_value))
    entry.pack(side=tk.LEFT)

    def update_entry(event):
        entry.delete(0, tk.END)
        entry.insert(0, str(slider.get()))

    slider.bind("<Motion>", update_entry)
    return slider, entry

b_slider, b_entry = create_slider_and_entry("Rozamiento (b):", 0.1, 1.0, b)
v0_slider, v0_entry = create_slider_and_entry("Velocidad inicial (v0):", 10, 100, v0)
u_slider, u_entry = create_slider_and_entry("Velocidad del viento (u):", 0, 100, u)
alfa_slider, alfa_entry = create_slider_and_entry("Dirección (alfa):", 0, 360, np.degrees(alfa))
h0_slider, h0_entry = create_slider_and_entry("Altura inicial (h0):", 0, 100, h0)
angulo_slider, angulo_entry = create_slider_and_entry("Ángulo de lanzamiento:", 0, 90, 20)

# Botón para actualizar la animación
ttk.Button(root, text="Actualizar Animación", command=get_values_and_update).pack()

# Ejecutar la aplicación
root.mainloop()