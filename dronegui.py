from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import tkinter as tk
import dronekit
from PIL import Image, ImageTk
from io import BytesIO
import numpy as np
import cv2
from mss import mss
from PIL import Image
import os
import dronekit_sitl
import torch
import pyautogui
import threading
import argparse



def screen_capture():
 global screen,screen_array,cropped_region,corrected_collors,results,model
 model = torch.hub.load('C:\Yolov7_instance_segmentation\yolov5', 'custom',
                        path='C:\Yolov7_instance_segmentation\yolov5\yolov5s.pt', source='local')
 while True:
    # Take a screenshot
    screen = pyautogui.screenshot()
    # Convert the output to a numpy array
    screen_array = np.array(screen)
    # Crop out the region we want - height, width, channels
    cropped_region = screen_array[0:830, 0:1420, :]
    # Convert the color channel order
    corrected_colors = cv2.cvtColor(cropped_region, cv2.COLOR_RGB2BGR)

    # Make detections
    results = model(corrected_colors)

    cv2.imshow('YOLO', np.squeeze(results.render()))

    # Cv2.waitkey
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Close down the frame
 cv2.destroyAllWindows()

def get_vehicle_info(vehicle):
    while True:
        print ("Altitude relative to home_location: %s" % vehicle.location.global_relative_frame.alt)
        print ("Heading: %s" % vehicle.heading)
        print ("Velocity: %s" % vehicle.velocity)
        print("\n")
        time.sleep(0.1)


def print_to_gui(vehicle, root, lon_label, alt_label, lat_label, yaw_label, pitch_label, roll_label,  battery_label,velocity_label,heading_label):
    while True:
        global lon
        lon= vehicle.location.global_relative_frame.lon
        global alt
        alt = vehicle.location.global_relative_frame.alt
        global lat
        lat = vehicle.location.global_frame.lat
        yaw = vehicle.attitude.yaw
        pitch = vehicle.attitude.pitch
        roll = vehicle.attitude.roll
        battery=vehicle.battery.level
        velocity=vehicle.velocity
        heading=vehicle.heading

        lon_label.config(text="Longitude: %s" % lon)
        alt_label.config(text="Altitude: %s" % alt)
        lat_label.config(text="Latitude: %s" % lat)
        yaw_label.config(text="Yaw: %s" % yaw)
        pitch_label.config(text="Pitch: %s" % pitch)
        roll_label.config(text="Roll: %s" % roll)
        battery_label.config(text='Battery: %s' % battery)
        velocity_label.config(text='Velocity: %s' % velocity)
        heading_label.config(text='Heading: %s' % heading)

        root.update()
def goto_location():
    lat1 = float(lat_entry.get())
    lon1 = float(lon_entry.get())
    alt1 = int(alt_entry.get())    
    target_location = LocationGlobalRelative(lat1, lon1, alt1)

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    print("Taking off!")
    vehicle.simple_takeoff(alt1)
    
    # define a function to be called repeatedly
    def travel_to_location():
        while True:
            if vehicle.location.global_relative_frame.alt >= alt1 * 0.95:
                #print('reached target altitude')
                vehicle.airspeed = 3
                vehicle.simple_goto(target_location)
                #print(f"Going to location ({lat}, {lon}, {alt})")
                
                if lon >= lon1 and lat >= lat1:
                    print('landing')
                    vehicle.mode = VehicleMode('LAND')
                    break
                else:
                    print('traveling to target location')
            else:
                print('taking off')
                
            time.sleep(1)

    threading.Thread(target=travel_to_location).start()
        

    # schedule the function to be called initially
    
    


    
'''    
def map_view(vehicle,root,map_widget):
 while True:
    # Get the current location of the UAV
    location = vehicle.location.global_frame

    # Update the map with the new location
    map_widget.set_marker(location.lat, location.lon, text="Drone", text_color="green",marker_color_circle="red", font=("Helvetica Bold", 24))
    
    # Wait for a short amount of time before updating again
    root.update()
'''
# Connect to the Pixhawk
#vehicle = connect('127.0.0.1:14550', wait_ready=True)

parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
print('connection string = %s'%connection_string)
vehicle = connect(connection_string, wait_ready=True)

'''
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()
vehicle = connect(connection_string, wait_ready=True)
'''

'''
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)
'''

root = tk.Tk()

'''
map_widget = TkinterMapView(root, width=400, height=300, corner_radius=0)
map_widget.pack()
'''
#Arka Plan Renginin ayarlanması
root.configure(bg='#2a283b')

#uygulama başlatıldığında windows çubuğunda açılan ikonun oluşturulması
#root.iconbitmap("C:\\Users\\LENOVO\\Desktop\\dd\\goknil.ico")

#Uygulama çerceve ismi ve pencere boyutarının belirlenmesi
root.title("GÖKNİL Quadcopter GCS Panel")
root.geometry("2400x1310+2390+0")


#Label'da yazılacak text ismi boyutu ve lokasyonunun belirlenmesi
label = tk.Label(root, text=" Quadcopter Flight Informations", font=('Courier New Baltic', 30), bg="#2a283b", fg='white')
label.pack(padx=20,  pady=20)


lat_label = tk.Label(root, text="Latitude:")
lat_label.place(x=0, y=300)
lat_entry = tk.Entry(root)
lat_entry.place(x=100, y=300)

lon_label = tk.Label(root, text="Longitude:")
lon_label.place(x=0, y=350)
lon_entry = tk.Entry(root)
lon_entry.place(x=100, y=350)

alt_label = tk.Label(root, text="Altitude:")
alt_label.place(x=0,y=400)
alt_entry = tk.Entry(root)
alt_entry.place(x=100, y=400)

go_button = tk.Button(root, text="Go to location", command=goto_location)
go_button.place(x=0, y=450)

lon_label = tk.Label(root, text="Longitude :", font=('Arial', 16), bg="#2a283b", fg='white')
lon_label.place(x=35, y=1100)

alt_label = tk.Label(root, text="Altitude:", font=('Arial', 16), bg="#2a283b", fg='white')
alt_label.place(x=35, y=1150)

lat_label = tk.Label(root, text="Latitude:", font=('Arial', 16), bg="#2a283b", fg='white')
lat_label.place(x=35, y=1200)

yaw_label = tk.Label(root, text="Yaw:", font=('Arial', 16), bg="#2a283b", fg='white')
yaw_label.place(x=35, y=1000)

pitch_label = tk.Label(root, text="Pitch:", font=('Arial', 16), bg="#2a283b", fg='white')
pitch_label.place(x=35, y=900)

roll_label = tk.Label(root, text="Roll:", font=('Arial', 16), bg="#2a283b", fg='white')
roll_label.place(x=35, y=950)

battery_label = tk.Label(root, text="Battery: %", font=('Arial', 20), bg="#2a283b", fg='green')
battery_label.place(x=2100, y=50)

heading_label = tk.Label(root, text="Heading:", font=('Arial', 16), bg="#2a283b", fg='sky blue')
heading_label.place(x=35, y=800)



'''
batterylevel_label = tk.Label(root, text="Battery > Level:", font=('Arial', 16), bg="#2a283b", fg='green')
batterylevel_label.place(x=1700, y=100)

batteryvoltage_label = tk.Label(root, text="Battery > Voltage:", font=('Arial', 16), bg="#2a283b", fg='sky blue')
batteryvoltage_label.place(x=1700, y=150)

batterycurrent_label = tk.Label(root, text="Battery > Current:", font=('Arial', 16), bg="#2a283b", fg='sky blue')
batterycurrent_label.place(x=1700, y=200)

ekf_label = tk.Label(root, text="EKF is Healthy:", font=('Arial', 16), bg="#2a283b", fg='green')
ekf_label.place(x=35, y=300)

lastheartbeat_label = tk.Label(root, text="Last Heartbeat:", font=('Arial', 16), bg="#2a283b", fg='green')
lastheartbeat_label.place(x=35, y=350)
'''

velocity_label = tk.Label(root, text="velocity:", font=('Arial', 16), bg="#2a283b", fg='red')
velocity_label.place(x=35, y=700)



#get_vehicle_info(vehicle=vehicle)

root.after(0, print_to_gui, vehicle, root,  lon_label, alt_label, lat_label, yaw_label, pitch_label,roll_label,battery_label,velocity_label,heading_label)

#root.after(0, map_view,vehicle,root,map_widget)
thread = threading.Thread(target=screen_capture)
thread.start()


root.mainloop()
