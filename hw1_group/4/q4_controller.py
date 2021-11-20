import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sym
from sympy.solvers import solve

#حرکت با توجه به مشخصات داده شده    
def forward_kinematic(phi1_dot ,phi2_dot ,r ,l):
    x_dot = r * ((phi1_dot + phi2_dot) / 2)
    y_dot = 0
    teta_dot =  r * ((phi1_dot - phi2_dot) / l)
    return ((x_dot, y_dot), teta_dot)


#تبدیل مشخصات دکارتی به قطبی
def decarti_to_polar(now, dest):
    delta_x = dest[0] - now[0]
    delta_y = dest[1] - now[1]
    p = math.sqrt(delta_x * delta_x + delta_y * delta_y)
    a = math.atan2(delta_y, delta_x) * 180 / math.pi - now[2]
    b = -now[2] - a
    return [p, a, b]

# مجاسبه سرعت و امگا توسط مطالب گفته شده توسط استاد
def velocity_omega(p, a, b, kp, ka, kb):
    v = kp * p
    w = ka * a + kb * b
    return v, w


#ثبت مکان جدید نقطه مد نظر با در نظر گرفتن مکان قبلی و ضرایب خطای داده شده
def place_calculation(goal, base):
    r = 2.05
    d = 5.5
    f = 64
    kp, ka, kb = [3, 8, -1.5]
    step_history = [base]
    for i in range(300):
        p, a, b = decarti_to_polar(step_history[-1], goal)
        v, w = velocity_omega(p, a, b, kp, ka, kb)
        phi_y, phi_x = invers_kinematics(v , w , r , d)
        phi_x = phi_x * 180 / math.pi
        phi_y = phi_y * 180 / math.pi
        last_place = forward(phi_x, phi_y , r ,d, f, step_history[-1])
        step_history.append(last_place)
    return step_history

#محاسبه ی مکان بعدی نقطه مد نظرمون
def forward(phi_x, phi_y, r, d, f, location) :
    x, y, theta = location
    dt = 1 / f
    x_r = r * (phi_y * math.pi / 180 + phi_x * math.pi / 180) / 2
    theta_dot = r * (phi_y - phi_x) / d
    u_r = [x_r, 0, theta_dot]
    angles = [
        [math.cos(math.pi / 180 * theta*(-1)),math.sin(math.pi / 180 * theta*(-1)), 0],
        [-math.sin(math.pi / 180 * theta*(-1)),math.cos(math.pi / 180 * theta*(-1)),0],
        [0, 0, 1],
    ]
    u_r = np.matmul(angles, u_r)
    new_position_x = x + dt * u_r[0]
    new_position_y = y + dt * u_r[1]
    new_position_theta = theta + dt * sai_i[2]
    return [new_position_x, new_position_y, new_position_theta]

#رسم مکان های پیموده شده
def plot(history):
    x = [record[0] for record in history]
    y = [record[1] for record in history]
    fig, ax = plt.subplots()
    fig.set_size_inches(6.4, 6)
    ax.xaxis.set_ticks(range(-6, 6))
    ax.yaxis.set_ticks(range(-6, 6))
    ax.scatter(x, y, s=2)
    ax.grid()
    circle1 = plt.Circle((0, 0), 5, color='r', fill=False)
    plt.gca().add_patch(circle1)
    plt.show()


#محاسبه تابع معکوس برای حرکت
def invers_kinematics(x_dot_r, theta_dot_r, r, d):
    x, y = sym.symbols('x,y')
    eq_1 = sym.Eq((x + y) * r / 2, x_dot_r)
    eq_2 = sym.Eq((x - y) * r / (2 * d), theta_dot_r * math.pi / 180)    
    res = solve([eq_1, eq_2], (x, y))
    phi_dot_1, phi_dot_2 = res.values()
    return [phi_dot_1, phi_dot_2]

    

goals = [
    [0, 0, 0],
    [5, 0, 0],
    [0, 5, 0],
    [0, -5, 0],
    [4, 3, 0],
    [-4, 3, 0],
    [-3, -4, 0],
    [3, -4, 0]
]
bases = [
    [-5, 0, 0],
    [0, 0, 90],
    [0, 0, 90],
    [0, 0, 90],
    [0, 0, 90],
    [0, 0, 90],
    [0, 0, 90],
    [0, 0, 90]
]
positions = []
for i in range (len(goals)):
    positions += place_calculation(goals[i], bases[i])
plot(positions)

while True:
    pass


