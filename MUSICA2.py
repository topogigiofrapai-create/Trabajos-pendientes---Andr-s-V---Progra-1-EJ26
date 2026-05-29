import tkinter as tk
from tkinter import ttk, messagebox
import threading, subprocess, os, signal, yt_dlp

p = None; play = False

def buscar():
    global p, play
    nom = ent.get().strip()
    if not nom or nom == "Busca una canción...": return
    if p: p.kill()
    lbl.config(text="🔍 Buscando..."); bar.start(10)
    def hilo():
        global p, play
        try:
            with yt_dlp.YoutubeDL({"quiet":True,"noplaylist":True}) as y:
                url = y.extract_info(f"ytsearch1:{nom}", download=False)["entries"][0]["webpage_url"]
            if os.path.exists("t.mp3"): os.remove("t.mp3")
            with yt_dlp.YoutubeDL({"format":"bestaudio/best","outtmpl":"t.%(ext)s","quiet":True,
                "postprocessors":[{"key":"FFmpegExtractAudio","preferredcodec":"mp3"}]}) as y:
                y.download([url])
            lbl.config(text=f"🎵 {nom}")
            p = subprocess.Popen(["ffplay","-nodisp","-autoexit","t.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            play = True; p.wait(); play = False; lbl.config(text="⏹ Listo")
        except Exception as e: messagebox.showerror("Error", str(e))
        finally: bar.stop()
    threading.Thread(target=hilo, daemon=True).start()

def pausa():
    global play
    if not p: return
    if play: p.send_signal(signal.SIGSTOP); play=False; btn_p.config(text="▶")
    else:    p.send_signal(signal.SIGCONT); play=True;  btn_p.config(text="⏸")

def stop(): 
    global p, play
    if p: p.kill(); p=None
    play=False; lbl.config(text="⏹ Detenido")

w = tk.Tk(); w.title("🎵 Reproductor"); w.configure(bg="#1a1a2e"); w.resizable(False,False)
ent = tk.Entry(w, font=("Helvetica",12), width=30, bg="#16213e", fg="white", insertbackground="white", relief="flat", bd=8)
ent.pack(pady=14)
ent.insert(0, "Busca una canción...")
ent.bind("<FocusIn>", lambda e: ent.delete(0,"end") if ent.get()=="Busca una canción..." else None)
ent.bind("<Return>", lambda e: buscar())
ent.focus()
bar = ttk.Progressbar(w, mode="indeterminate", length=320); bar.pack()
lbl = tk.Label(w, text="⏹ Detenido", bg="#1a1a2e", fg="#a8a8b3", font=("Helvetica",11)); lbl.pack(pady=6)
f = tk.Frame(w, bg="#1a1a2e"); f.pack(pady=8)
tk.Button(f, text="Buscar", command=buscar, bg="#e94560", fg="white", font=("Helvetica",11,"bold"), relief="flat", padx=10, cursor="hand2").pack(side="left", padx=6, ipady=4)
btn_p = tk.Button(f, text="▶", command=pausa, bg="#0f3460", fg="white", font=("Helvetica",13,"bold"), relief="flat", width=4, cursor="hand2"); btn_p.pack(side="left", padx=6, ipady=4)
tk.Button(f, text="⏹", command=stop, bg="#0f3460", fg="white", font=("Helvetica",13,"bold"), relief="flat", width=4, cursor="hand2").pack(side="left", padx=6, ipady=4)
w.update_idletasks()
x = (w.winfo_screenwidth() // 2) - (w.winfo_width() // 2)
y = (w.winfo_screenheight() // 2) - (w.winfo_height() // 2)
w.geometry(f"+{x}+{y}")
w.mainloop()

def cerrar():
    if p: p.kill()
    w.destroy()
w.protocol("WM_DELETE_WINDOW", cerrar)