from pynput import mouse
import time

print("==================================================")
print("   ORBITAL PATHFINDER - MONITOR              ")
print("==================================================")
print("Status: RUNNING. Every click will be logged below.")
print("If you click and see NOTHING, run this as Admin.")
print("--------------------------------------------------")

# Track timings to detect electrical shorts
last_press_time = {}

def on_click(x, y, button, pressed):
    # 1. IMMEDIATE LOGGING (So you know it works)
    state_str = "DOWN" if pressed else "UP  "
    timestamp = time.time()
    readable_time = time.strftime('%H:%M:%S', time.localtime(timestamp)) + f".{int((timestamp % 1) * 1000):03d}"
    
    print(f"[{readable_time}] {button} {state_str}", end="")
    
    # 2. ANALYSIS (Only on button DOWN)
    if pressed:
        last_press_time[button] = timestamp
        
        # CHECK: Did M3 fire exactly when M1 or M2 fired? (Hardware Short)
        if button == mouse.Button.middle:
            t_left = last_press_time.get(mouse.Button.left, 0)
            t_right = last_press_time.get(mouse.Button.right, 0)
            
            # If M3 happened less than 40ms after Left/Right
            if abs(timestamp - t_left) < 0.04:
                print(" <--- !!! SHORT CIRCUIT (Synced w/ LEFT) !!!", end="")
            elif abs(timestamp - t_right) < 0.04:
                print(" <--- !!! SHORT CIRCUIT (Synced w/ RIGHT) !!!", end="")
            else:
                print(" <--- Independent Click (Software/Switch)", end="")

    print() # New line

# Start the listener
# suppress=False means it lets clicks pass through to your PC normally
with mouse.Listener(on_click=on_click, suppress=False) as listener:
    listener.join()