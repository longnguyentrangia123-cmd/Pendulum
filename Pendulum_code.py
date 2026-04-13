# importing libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation

class Pendulum():
    def __init__(self, angle_radian = 0.5, g = 9.81, length_pendulum = 1.0, total_time = 20, steps = 500, damping = 0.5):    # setting initial variables
        self.angle_radian = angle_radian
        self.initial_angle_radian = angle_radian
        self.g = g
        self.length_pendulum = length_pendulum
        self.initial_length_pendulum = length_pendulum
        self.total_time = total_time
        self.steps = steps
        self.damping = damping
        self.initial_damping = damping

        self.angular_velocity = 0.0
        self.angular_acceleration = 0.0
        self.time = 0.0
        self.current_frame = 0

        self.dt = self.total_time/self.steps

        self.angle_radian_history = []
        self.angular_velocity_history = []
        self.angular_acceleration_history = []
        self.time_history = []

        self.is_paused = False

    def compute(self):  # calculating values and assigning it to lists
        # assigning initial values into lists
        self.angle_radian_history.append(self.angle_radian)
        self.angular_velocity_history.append(self.angular_velocity)
        self.angular_acceleration_history.append(self.angular_acceleration)
        self.time_history.append(self.time)

        while self.time < self.total_time: 
            self.angular_acceleration = -(self.g / self.length_pendulum) * np.sin(self.angle_radian) - self.damping * self.angular_velocity

            self.angular_velocity += self.angular_acceleration * self.dt
            self.angle_radian += self.angular_velocity * self.dt    
            self.time += self.dt

            # assigning calculated values into lists
            self.angle_radian_history.append(self.angle_radian)
            self.angular_velocity_history.append(self.angular_velocity)
            self.angular_acceleration_history.append(self.angular_acceleration)
            self.time_history.append(self.time)
            

    def setup_figure(self):  # setting up the whole figure
        self.fig = plt.figure(figsize= (10,8))
        self.fig.suptitle("Pendulum", fontsize = 20, fontweight = "bold")

        gs = self.fig.add_gridspec(4,1, height_ratios = [1.5,1,1,1], left = 0.1, bottom = 0.3, right = 0.9, top = 0.92, hspace = 1)

        self.ax_animation = self.fig.add_subplot(gs[0])
        self.setup_animation_pendulum()

        self.ax_angle_radian_graph = self.fig.add_subplot(gs[1])
        self.setup_angle_radian_graph()

        self.ax_angular_velocity_graph = self.fig.add_subplot(gs[2])
        self.setup_angular_velocity_graph()

        self.ax_angular_acceleration_graph = self.fig.add_subplot(gs[3])
        self.setup_angular_acceleration_graph()

        self.setup_sliders()

        self.setup_buttons()


    def setup_animation_pendulum(self):  # setting up the animation of the pednulum
        self.ax_animation.set_xlim(-self.length_pendulum, self.length_pendulum)
        self.ax_animation.set_ylim(-self.length_pendulum - 0.5, self.length_pendulum + 0.5)
        self.ax_animation.set_aspect('equal') 
        self.ax_animation.axis('off')

        self.ax_animation.plot([-0.1, 0.1], [0.1, 0.1], 'k-', linewidth=5)

        self.pendulum_line, = self.ax_animation.plot([], [], 'o-')

    
    def setup_angle_radian_graph(self):  # setting up the angle graph animation 
        self.ax_angle_radian_graph.set_title("Angle (rad) - Time (s)")
        self.ax_angle_radian_graph.set_xlabel("Time")
        self.ax_angle_radian_graph.set_ylabel("Angle")
        self.ax_angle_radian_graph.set_xlim(0, self.total_time)
        self.ax_angle_radian_graph.set_ylim(min(self.angle_radian_history), max(self.angle_radian_history))

        self.angle_radian_graph_animation, = self.ax_angle_radian_graph.plot([], [])


    def setup_angular_velocity_graph(self):  # setting up the angular velocity graph animation
        self.ax_angular_velocity_graph.set_title("Angular velocity (rad/s) - Time (s)")
        self.ax_angular_velocity_graph.set_xlabel("Time")
        self.ax_angular_velocity_graph.set_ylabel("Angular velocity")
        self.ax_angular_velocity_graph.set_xlim(0, self.total_time)
        self.ax_angular_velocity_graph.set_ylim(min(self.angular_velocity_history), max(self.angular_velocity_history))

        self.angular_velocity_graph_animation, = self.ax_angular_velocity_graph.plot([], [])


    def setup_angular_acceleration_graph(self):  # setting up the angular acceleration graph animation
        self.ax_angular_acceleration_graph.set_title("Angular acceleration (rad/s/s) - Time (s)")
        self.ax_angular_acceleration_graph.set_xlabel("Time")
        self.ax_angular_acceleration_graph.set_ylabel("Angular acceleration")
        self.ax_angular_acceleration_graph.set_xlim(0, self.total_time)
        self.ax_angular_acceleration_graph.set_ylim(min(self.angular_acceleration_history), max(self.angular_acceleration_history))

        self.angular_acceleration_graph_animation, = self.ax_angular_acceleration_graph.plot([], [])


    def animate(self, _):  # adding animation
        self.current_frame += 1

        if self.current_frame >= len(self.time_history):  # stopping animation when the last value of the lists are reached
            self.animation.event_source.stop()
            return (self.angle_radian_graph_animation, self.angular_velocity_graph_animation, self.angular_acceleration_graph_animation, self.pendulum_line)

        i = self.current_frame

        # animation for pendulum
        x = self.length_pendulum * np.sin(self.angle_radian_history[i])
        y = -self.length_pendulum * np.cos(self.angle_radian_history[i])
        self.pendulum_line.set_data([0, x], [0.1, y])

        # animation for graphs
        self.angle_radian_graph_animation.set_data(self.time_history[:i], self.angle_radian_history[:i])
        self.angular_velocity_graph_animation.set_data(self.time_history[:i], self.angular_velocity_history[:i])
        self.angular_acceleration_graph_animation.set_data(self.time_history[:i], self.angular_acceleration_history[:i])

        return (self.angle_radian_graph_animation, self.angular_velocity_graph_animation, self.angular_acceleration_graph_animation, self.pendulum_line)


    def setup_sliders(self):  # setting up sliders
        ax_initial_angle = plt.axes([0.15, 0.15, 0.7, 0.05])
        self.initial_angle_slider = Slider(ax_initial_angle, "Initial angle", valmax = np.pi, valmin = 0.1, valinit = self.initial_angle_radian)

        ax_length_pendulum = plt.axes([0.15, 0.1, 0.7, 0.05])
        self.length_pendulum_slider = Slider(ax_length_pendulum, "Pendulum length", valmax = 5, valmin = 1, valinit = self.length_pendulum)

        ax_damping = plt.axes([0.15, 0.05, 0.7, 0.05])
        self.damping_slider = Slider(ax_damping, "Damping", valmax = 5, valmin = 0, valinit = self.damping)


    def setup_buttons(self):  # setting up buttons
        ax_reset = plt.axes([0.9, 0.01, 0.075, 0.04])
        self.reset_button = Button(ax_reset, "Reset")
        self.reset_button.on_clicked(self.reset)

        ax_run = plt.axes([0.81, 0.01, 0.075, 0.04])
        self.run_button = Button(ax_run, "Update")
        self.run_button.on_clicked(self.update_parameter)

        ax_toggle_pause = plt.axes([0.72, 0.01, 0.075, 0.04])
        self.toggle_pause_button = Button(ax_toggle_pause, "Pause")
        self.toggle_pause_button.on_clicked(self.toggle_pause)

        ax_return = plt.axes([0.63, 0.01, 0.075, 0.04])
        self.return_button = Button(ax_return, "Return")
        self.return_button.on_clicked(self.close_window)

    
    def reset(self, event = None):  # actions when reset button is pressed
        print("Reset button pressed. \n")

        self.angle_radian = self.initial_angle_radian
        self.length_pendulum = self.initial_length_pendulum
        self.damping = self.initial_damping

        self.initial_angle_slider.set_val(self.initial_angle_radian)
        self.length_pendulum_slider.set_val(self.initial_length_pendulum)
        self.damping_slider.set_val(self.initial_damping)
        
        self.reset_graph()


    def toggle_pause(self, event = None):  # actions when pause/resume button is pressed
        if self.is_paused:
            print("Resuming animation. \n")
            self.animation.event_source.start()
            self.toggle_pause_button.label.set_text("Pause")
            self.is_paused = False

        else:
            print("Pausing animation. \n")
            self.animation.event_source.stop()
            self.toggle_pause_button.label.set_text("Resume")
            self.is_paused = True


    def update_parameter(self, val):  # actions when update button is pressed
        print("Update button pressed. \n")

        self.angle_radian = self.initial_angle_slider.val
        self.length_pendulum = self.length_pendulum_slider.val
        self.damping = self.damping_slider.val

        self.reset_graph()

    
    def close_window(self, event = None):  # actions when return button is pressed
        print("Closing window. \n")
        plt.close(self.fig)

    def reset_graph(self, event = None):  # resetting the graph (clearing)
        
        self.animation.event_source.stop()  # stopping animation

        # resetting values
        self.current_frame = 0
        self.time = 0.0
        self.angular_velocity = 0.0
        self.angular_acceleration = 0.0

        self.angle_radian_history = []
        self.angular_velocity_history = []
        self.angular_acceleration_history = []
        self.time_history = []

        self.angle_radian_graph_animation.set_data([], [])
        self.angular_velocity_graph_animation.set_data([], [])
        self.angular_acceleration_graph_animation.set_data([], [])
        
        self.compute()
        self.ax_angle_radian_graph.set_ylim(min(self.angle_radian_history), max(self.angle_radian_history))
        self.ax_angular_velocity_graph.set_ylim(min(self.angular_velocity_history), max(self.angular_velocity_history))
        self.ax_angular_acceleration_graph.set_ylim(min(self.angular_acceleration_history), max(self.angular_acceleration_history))

        self.run()
        self.fig.canvas.draw_idle()


    def run(self):  # run the animation
        self.animation = FuncAnimation(self.fig, self.animate, frames = len(self.time_history), interval = 50)

        plt.show()


is_running = True
while is_running:
    option = input("""Pendulum animation: 
    r to run
    q to quit
      > """)
    match option:
        case "r": 
            program = Pendulum()
            program.compute()
            program.setup_figure()
            program.run()

        case "q":
            is_running = False

