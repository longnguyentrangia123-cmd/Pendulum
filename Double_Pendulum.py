import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from matplotlib.animation import FuncAnimation


class DoublePendulum():
    def __init__(self,
                 angle1_radian=0.5,
                 angle2_radian=0.5,
                 g=9.81,
                 length1_pendulum=1.0,
                 length2_pendulum=1.0,
                 mass1=1.0,
                 mass2=1.0,
                 total_time=20,
                 steps=1000):

        self.angular_velocity1 = 0.0
        self.angular_velocity2 = 0.0

        self.angle1_radian = angle1_radian
        self.angle2_radian = angle2_radian
        self.initial_angle1_radian = angle1_radian
        self.initial_angle2_radian = angle2_radian
        self.g = g
        self.length1_pendulum = length1_pendulum
        self.length2_pendulum = length2_pendulum
        self.initial_length1_pendulum = length1_pendulum
        self.initial_length2_pendulum = length2_pendulum
        self.mass1 = mass1
        self.mass2 = mass2

        self.total_time = total_time
        self.steps = steps
        self.dt = self.total_time / self.steps


        self.time = 0.0
        self.current_frame = 0


        self.angle1_history = []
        self.angle2_history = []
        self.time_history = []

        self.is_paused = False


    def derivatives(self, state):
        theta1, omega1, theta2, omega2 = state

        delta = theta1 - theta2

        denom = (2*self.mass1 + self.mass2 -
                 self.mass2 * np.cos(2*delta))

        a1 = (
            -self.g*(2*self.mass1 + self.mass2)*np.sin(theta1)
            - self.mass2*self.g*np.sin(theta1 - 2*theta2)
            - 2*np.sin(delta)*self.mass2*(
                omega2**2 * self.length2_pendulum +
                omega1**2 * self.length1_pendulum * np.cos(delta)
            )
        ) / (self.length1_pendulum * denom)

        a2 = (
            2*np.sin(delta)*(
                omega1**2 * self.length1_pendulum * (self.mass1 + self.mass2)
                + self.g*(self.mass1 + self.mass2)*np.cos(theta1)
                + omega2**2 * self.length2_pendulum * self.mass2 * np.cos(delta)
            )
        ) / (self.length2_pendulum * denom)

        return np.array([omega1, a1, omega2, a2])


    def compute(self):
        state = np.array([
            self.angle1_radian,
            self.angular_velocity1,
            self.angle2_radian,
            self.angular_velocity2
        ])

        self.angle1_history.append(state[0])
        self.angle2_history.append(state[2])
        self.time_history.append(self.time)

        while self.time < self.total_time:
            dt = self.dt

            k1 = self.derivatives(state)
            k2 = self.derivatives(state + 0.5 * dt * k1)
            k3 = self.derivatives(state + 0.5 * dt * k2)
            k4 = self.derivatives(state + dt * k3)

            state = state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

            self.time += dt

            self.angle1_history.append(state[0])
            self.angle2_history.append(state[2])
            self.time_history.append(self.time)


        self.angle1_radian = state[0]
        self.angular_velocity1 = state[1]
        self.angle2_radian = state[2]
        self.angular_velocity2 = state[3]


    def setup_figure(self):
        self.fig = plt.figure(figsize=(14, 8))
        self.fig.suptitle("Double Pendulum (RK4)", fontsize=18, fontweight="bold")

        gs = self.fig.add_gridspec(4, 1, height_ratios = [5, 1, 1, 1])

        self.ax_animation = self.fig.add_subplot(gs[0])
        self.setup_animation()

        self.setup_sliders()

        self.setup_buttons()


    def setup_animation(self):
        max_length = self.length1_pendulum + self.length2_pendulum

        self.ax_animation.set_xlim(-max_length, max_length)
        self.ax_animation.set_ylim(-max_length, max_length)
        self.ax_animation.set_aspect('equal')
        self.ax_animation.axis('off')

        self.line, = self.ax_animation.plot([], [], 'o-', lw=2)


    def animate(self, _):
        self.current_frame += 1

        if self.current_frame >= len(self.time_history):
            self.animation.event_source.stop()
            return (self.line,)

        i = self.current_frame

        x1 = self.length1_pendulum * np.sin(self.angle1_history[i])
        y1 = -self.length1_pendulum * np.cos(self.angle1_history[i])

        x2 = x1 + self.length2_pendulum * np.sin(self.angle2_history[i])
        y2 = y1 - self.length2_pendulum * np.cos(self.angle2_history[i])

        self.line.set_data([0, x1, x2], [0, y1, y2])

        return (self.line,)


    def setup_sliders(self):
        ax_initial_position1 = plt.axes([0.15, 0.25, 0.7, 0.05])
        self.initial_position1_slider = Slider(ax_initial_position1, "Initial position 1", valinit = self.initial_angle1_radian, valmax = np.pi, valmin = 0)

        ax_initial_position2 = plt.axes([0.15, 0.2, 0.7, 0.05])
        self.initial_position2_slider = Slider(ax_initial_position2, "Initial position 2", valinit = self.initial_angle2_radian, valmax = np.pi, valmin = 0)

        ax_length_pendulum1 = plt.axes([0.15, 0.15, 0.7, 0.05])
        self.length_pendulum1_slider = Slider(ax_length_pendulum1, "Length pendulum 1", valinit = self.length1_pendulum, valmax = 1.5, valmin = 0.1)

        ax_length_pendulum2 = plt.axes([0.15, 0.1, 0.7, 0.05])
        self.length_pendulum2_slider = Slider(ax_length_pendulum2, "Length pendulum 2", valinit = self.length2_pendulum, valmax = 1.5, valmin = 0.1)


    def setup_buttons(self):
        ax_update = plt.axes([0.58, 0.02, 0.1, 0.05])
        self.update_button = Button(ax_update, "Update")
        self.update_button.on_clicked(self.update)

        ax_reset = plt.axes([0.8, 0.02, 0.1, 0.05])
        self.reset_button = Button(ax_reset, "Reset")
        self.reset_button.on_clicked(self.reset)

        ax_pause = plt.axes([0.69, 0.02, 0.1, 0.05])
        self.pause_button = Button(ax_pause, "Pause")
        self.pause_button.on_clicked(self.toggle_pause)

    
    def update(self, val):
        print("Update button pressed. \n")
        self.angle1_radian = self.initial_position1_slider.val
        self.angle2_radian = self.initial_position2_slider.val
        self.length1_pendulum = self.length_pendulum1_slider.val
        self.length2_pendulum = self.length_pendulum2_slider.val

        self.reset_graph()


    def reset(self, event=None):
        print("Reset button pressed. \n")

        self.angle1_radian = self.initial_angle1_radian
        self.angle2_radian = self.initial_angle2_radian
        self.length1_pendulum = self.initial_length1_pendulum
        self.length2_pendulum = self.initial_length2_pendulum

        self.initial_position1_slider.set_val(self.initial_angle1_radian)
        self.initial_position2_slider.set_val(self.initial_angle2_radian)
        self.length_pendulum1_slider.set_val(self.initial_length1_pendulum)
        self.length_pendulum2_slider.set_val(self.initial_length2_pendulum)

        self.reset_graph()


    def toggle_pause(self, event=None):
        if self.is_paused:
            self.animation.event_source.start()
            self.pause_button.label.set_text("Pause")
            self.is_paused = False
        else:
            self.animation.event_source.stop()
            self.pause_button.label.set_text("Resume")
            self.is_paused = True


    def reset_graph(self):
        self.animation.event_source.stop()

        self.current_frame = 0
        self.time = 0.0

        self.angular_velocity1 = 0.0
        self.angular_velocity2 = 0.0

        self.angle1_history = []
        self.angle2_history = []
        self.time_history = []

        self.line.set_data([], [])

        self.compute()
        
        self.animation.event_source.start()


    def run(self):
        self.animation = FuncAnimation(
            self.fig,
            self.animate,
            frames=len(self.time_history),
            interval=20
        )
        plt.show()



is_running = True

while is_running:
    option = input("""Double Pendulum:
    r to run
    q to quit
    > """)

    match option:
        case "r":
            program = DoublePendulum()
            program.compute()
            program.setup_figure()
            program.run()

        case "q":
            is_running = False


