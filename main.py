import customtkinter as ctk
import random
import time
import threading
import matplotlib.pyplot as plt

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -------------------------
# Data
# -------------------------
real_users = {
    "user1": "pass123",
    "admin": "admin123",
    "anjana": "secure@123"
}

leaked_credentials = [
    ("user1", "123456"),
    ("admin", "admin123"),
    ("anjana", "password"),
    ("user1", "pass123"),
]

locations = ["India", "USA", "Russia", "China"]

# -------------------------
# Globals
# -------------------------
attack_running = False
defense_enabled = False
attempts = 0
success = 0
attempt_history = []

# -------------------------
# Logging
# -------------------------
def log(msg):
    app.after(0, lambda: log_box.insert("end", msg + "\n\n"))
    app.after(0, lambda: log_box.see("end"))

# -------------------------
# Risk Logic
# -------------------------
def calculate_risk():
    risk = 0
    if attempts > 2:
        risk += 30
    if random.choice([True, False]):
        risk += 30
    if attempts > 4:
        risk += 40
    return risk

def defense_action(risk):
    if not defense_enabled:
        return "No Defense"
    if risk < 30:
        return "Allowed"
    elif risk < 60:
        return "CAPTCHA"
    elif risk < 80:
        return "OTP"
    else:
        return "BLOCK"

# -------------------------
# Manual Login
# -------------------------
def manual_login():
    user = username.get()
    pwd = password.get()

    if user in real_users and real_users[user] == pwd:
        log(f"✅ Login Success: {user}")
    else:
        log(f"❌ Login Failed: {user}")

# -------------------------
# Attack Simulation
# -------------------------
def attack():
    global attack_running, attempts, success

    attack_running = True
    attempts = 0
    success = 0
    attempt_history.clear()

    log("🚨 Attack Started...")

    for u, p in leaked_credentials:
        if not attack_running:
            break

        attempts += 1
        attempt_history.append(attempts)
        loc = random.choice(locations)

        log(f"[{attempts}] Trying {u}:{p} from {loc}")

        if u in real_users and real_users[u] == p:
            success += 1
            log(f"✅ SUCCESS LOGIN: {u}")

        risk = calculate_risk()
        action = defense_action(risk)

        log(f"⚠️ Risk Score: {risk} → {action}")

        update_dashboard()

        if action == "BLOCK":
            log("🛑 BLOCKED: Attack stopped")
            break

        time.sleep(1)

# -------------------------
# Controls
# -------------------------
def start_attack():
    threading.Thread(target=attack, daemon=True).start()

def stop_attack():
    global attack_running
    attack_running = False
    log("⛔ Attack stopped by user")

def toggle_defense():
    global defense_enabled
    defense_enabled = not defense_enabled
    status = "ON" if defense_enabled else "OFF"

    status_label.configure(text=f"Defense: {status}")
    log(f"🛡️ Defense turned {status}")

# -------------------------
# Graph
# -------------------------
def show_graph():
    if not attempt_history:
        log("⚠️ No data to plot")
        return

    plt.figure()
    plt.plot(attempt_history)
    plt.title("Attack Attempts Over Time")
    plt.xlabel("Attempt Number")
    plt.ylabel("Attempts")
    plt.grid()
    plt.show()

# -------------------------
# Dashboard Update
# -------------------------
def update_dashboard():
    app.after(0, lambda: attempts_label.configure(text=str(attempts)))
    app.after(0, lambda: success_label.configure(text=str(success)))

# -------------------------
# UI
# -------------------------
app = ctk.CTk()
app.geometry("1100x700")
app.title("Cyber Range Dashboard")

# Sidebar
sidebar = ctk.CTkFrame(app, width=200)
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(sidebar, text="Cyber Range", font=("Arial", 18)).pack(pady=20)

ctk.CTkButton(sidebar, text="Start Attack", command=start_attack).pack(pady=10)
ctk.CTkButton(sidebar, text="Stop Attack", command=stop_attack).pack(pady=10)
ctk.CTkButton(sidebar, text="Toggle Defense", command=toggle_defense).pack(pady=10)
ctk.CTkButton(sidebar, text="Show Graph", command=show_graph).pack(pady=10)

status_label = ctk.CTkLabel(sidebar, text="Defense: OFF")
status_label.pack(pady=20)

# Main Area
main = ctk.CTkFrame(app)
main.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Title
ctk.CTkLabel(main, text="Credential Stuffing vs Adaptive Authentication", font=("Arial", 18)).pack(pady=10)

# ✅ Valid Credentials Display
info_label = ctk.CTkLabel(
    main,
    text="Valid Login → admin/admin123  |  anjana/secure@123",
    text_color="lightgreen"
)
info_label.pack(pady=5)

# Dashboard Cards
card_frame = ctk.CTkFrame(main)
card_frame.pack(fill="x", pady=10)

attempts_label = ctk.CTkLabel(card_frame, text="0", font=("Arial", 20))
attempts_label.grid(row=0, column=0, padx=50)

success_label = ctk.CTkLabel(card_frame, text="0", font=("Arial", 20))
success_label.grid(row=0, column=1, padx=50)

ctk.CTkLabel(card_frame, text="Attempts").grid(row=1, column=0)
ctk.CTkLabel(card_frame, text="Success").grid(row=1, column=1)

# Login Section
login_frame = ctk.CTkFrame(main)
login_frame.pack(pady=10)

username = ctk.CTkEntry(login_frame, placeholder_text="Username", width=200)
username.grid(row=0, column=0, padx=10)

password = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=200)
password.grid(row=0, column=1, padx=10)

ctk.CTkButton(login_frame, text="Login", command=manual_login).grid(row=0, column=2, padx=10)

# Logs (BIG)
log_box = ctk.CTkTextbox(main, width=850, height=400)
log_box.pack(pady=20)

app.mainloop()