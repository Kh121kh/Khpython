from ctypes import *
import streamlit as st
from time import sleep
from PIL import Image
import requests
import threading
from queue import Queue
from drawnow import *
import numpy as np  # import numpy library
import matplotlib.pyplot as plt  # import matplotlib


# Load the K8055D.dll library
k8055 = WinDLL("K8055D.dll")

# Open the connection to the K8055 board
k8055.OpenDevice()
global q
q=Queue()
# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Create the Streamlit app


def main():

    # Set Streamlit app title
    st.title("K8055 Control App")
    # with open('style.css') as f:
    # st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    container = st.container()
    image1 = Image.open("pandasFuny.jpg")
    image2=Image.open("k8055.jpg")
    container.image(image1, width=200)
    st.sidebar.image(image2, width=300)
    container.write(" # Data Analysis and Visualization # ")

############################ trying st.metric#########
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature:sunglasses:", "70 °F", "1.2 °F")
    col2.metric("Wind:+1:", "9 mph", "-8%")
    col3.metric("Humidity:-1:", "86%", "4%")
######################################################

    # Define the function to handle button click

    def handle_button_click(channel, x):
        # Toggle the output on the specified channel

        if x:
            k8055.SetDigitalChannel(channel)
        else:
            k8055.ClearDigitalChannel(channel)

    # Define the function to handle button click
    def handle_button_click_all_on():
        # Toggle the output on the specified channel
        k8055.SetAllDigital()

    def handle_button_click_all_off():
        # Toggle the output on the specified channel
        k8055.ClearAllDigital()

    def makeFig():  # Create a function that makes our desired plot
        plt.ylim(0, 300)  # Set y min and max values
        plt.title('Live Streaming Voltage Data')  # Plot the title
        plt.grid(True)  # Turn the grid on
        plt.ylabel('Ch1 (V)')  # Set ylabels
        plt.plot(Ch1_v, 'ro-', label='Ch1 (V)')  # plot channel 1 voltage
        plt.legend(loc='upper left')  # plot the legend
        plt2 = plt.twinx()  # Create a second y axis
        plt.ylim(0, 300)  # Set limits of second y axis- adjust to readings you are getting
        plt2.plot(Ch2_v, 'b^-', label='Ch2 (V)')  # plot channel 2 voltage
        plt2.set_ylabel('Ch2 (V)')  # label second y axis
        plt2.ticklabel_format(useOffset=False)  # Force matplotlib to NOT autoscale y axis
        plt2.legend(loc='upper right')  # plot the legend
        st.pyplot(plt)

    for i in range(8):
        if f"state_{i+1}" not in st.session_state:
            st.session_state[f'state_{i+1}']=False
    if "data1" not in st.session_state:
        st.session_state["data1"]=0
    if "data2" not in st.session_state:
        st.session_state["data2"] = 0

    # Create the sidebar
    st.sidebar.title("LED Control")

    # Create buttons for each LED in three columns
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        if st.button("LED 1"):
            if not st.session_state.state_1:
                st.session_state.state_1=True
            else:
                st.session_state.state_1 = False
            handle_button_click(1,st.session_state.state_1)
        if st.button("LED 4"):
            if not st.session_state.state_4:
                st.session_state.state_4=True
            else:
                st.session_state.state_4 = False
            handle_button_click(4,st.session_state.state_4)
        if st.button("LED 7"):
            if not st.session_state.state_7:
                st.session_state.state_7=True
            else:
                st.session_state.state_7 = False
            handle_button_click(7,st.session_state.state_7)
    with col2:
        if st.button("LED 2"):
            if not st.session_state.state_2:
                st.session_state.state_2=True
            else:
                st.session_state.state_2 = False
            handle_button_click(2,st.session_state.state_2)
        if st.button("LED 5"):
            if not st.session_state.state_5:
                st.session_state.state_5=True
            else:
                st.session_state.state_5 = False
            handle_button_click(5,st.session_state.state_5)
        if st.button("LED 8"):
            if not st.session_state.state_8:
                st.session_state.state_8=True
            else:
                st.session_state.state_8 = False
            handle_button_click(8,st.session_state.state_8)
    with col3:
        if st.button("LED 3"):
            if not st.session_state.state_3:
                st.session_state.state_3=True
            else:
                st.session_state.state_3 = False
            handle_button_click(3,st.session_state.state_3)
        if st.button("LED 6"):
            if not st.session_state.state_6:
                st.session_state.state_6=True
            else:
                st.session_state.state_6 = False
            handle_button_click(6,st.session_state.state_6)
        if st.button("ALL ON"):
            handle_button_click_all_on()
            for i in range(8):
                st.session_state[f'state_{i+1}']=True
    if st.sidebar.button("ALL OFF",use_container_width=True):
        handle_button_click_all_off()
        for i in range(8):
            st.session_state[f'state_{i + 1}'] = False
    if st.sidebar.button("FLASHING"):
        for i in range(5):
            handle_button_click_all_on()
            for i in range(8):
                st.session_state[f'state_{i + 1}'] = True
            sleep(0.2)
            handle_button_click_all_off()
            for i in range(8):
                st.session_state[f'state_{i + 1}'] = False
            sleep(0.2)

    # st.session_state["digital_inputs"]=q.get()
    # st.write(st.session_state)
########### Plotting sine and cosine #############
    # x = np.linspace(0, 2 * np.pi, 20)  # create your x array
    # y = np.sin(x)  # create y array
    # z = np.cos(x)  # create z array
    # # y=[0.5,0.4,0.3,0.2,0.5,0.7,0.5,0.6,0.1,0.4,0.8,0.9,0.4,0.5,0.6,0.8,0.2,0.5,0.2,0.4]
    # # z=[0.4,0.1,0.2,0.2,0.3,0.6,0.8,0.3,0.8,0.9,0.3,0.5,0.7,0.3,0.5,0.3,0.7,0.9,0.1,0.4]
    # # plt.plot(x,y, 'b-d', linewidth=2, label='sinx') #plot y
    # # plt.plot(x,z, 'r-o', linewidth=2, label='cosx') #plot z
    # plt.plot(x, y, 'b-d', linewidth=2, label='y data')  # plot y
    # plt.plot(x, z, 'r-o', linewidth=2, label='z data')  # plot z
    # plt.grid(True)  # display background grid
    # plt.axis([0, 2 * np.pi, -1.5, 1.5])  # set range on axis
    # plt.title('My Sin and Cos Waves')  # chart title
    # # plt.axis([0,2*np.pi,0,1.0]) #set range on axis
    # # plt.title('My y data and z data') #chart title
    # plt.xlabel('Time in Seconds')  # label x axis
    # plt.ylabel('My Waves')  # label y axis
    # plt.legend()  # show legend
    # # plt.show()  # show the plot
    # st.pyplot(plt)
    ########## Showing analag voltages ##########
    Ch1_v = []
    Ch2_v = []

    plt.ion()  # Tell matplotlib you want interactive mode to plot live data
    cnt = 0
    if st.sidebar.button("show analog voltages"):
        st.session_state.data1 = k8055.ReadAnalogChannel(1)
        st.session_state.data2 = k8055.ReadAnalogChannel(2)

        Ch1_v.append(st.session_state.data1 )  # Build our Ch1_v array by appending temp readings
        Ch2_v.append(st.session_state.data2)  # Building our Ch2_v array by appending P readings
        drawnow(makeFig)  # Call drawnow to update our live graph
        plt.pause(.000001)  # Pause Briefly. Important to keep drawnow from crashing
        cnt = cnt + 1
        if (cnt > 50):  # If you have 50 or more points, delete the first one from the array
            Ch1_v.pop(0)  # This allows us to just see the last 50 data points
            Ch2_v.pop(0)


        st.slider('Position', 0, 255, value=st.session_state.data1)
        st.checkbox("any",value=k8055.ReadDigitalChannel(1),key='a')
        st.checkbox("any", value=k8055.ReadDigitalChannel(2),key='b')


# Run the Streamlit app
if __name__ == "__main__":
    main()