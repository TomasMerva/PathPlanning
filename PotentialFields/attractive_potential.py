import math
import matplotlib.pyplot as plt
import numpy as np
import time

# return gradient of q
def QuadraticAttractivePotential(q, q_goal, zeta):
    return zeta*(q-q_goal)

# return gradient of cubic potential
def ConicAttractivePotential(q, q_goal, zeta):
    delta = q - q_goal
    l2 = np.linalg.norm(delta, 2)
    return (zeta*delta)/l2


# Combination of Quadratic and Conic potential based on the distance to goal treshold
def CombAttractivePotential(q, q_goal, zeta):
    d_goal = 2.0
    l2 = np.linalg.norm((q, q_goal), 2)
    if l2 <= d_goal:
        return QuadraticAttractivePotential(q, q_goal, zeta)
    else:
        return d_goal*ConicAttractivePotential(q, q_goal, zeta)



# Input: a means to compute the gradient at a point q
# Ouput: A sequence of points { q(0), q(1), ..., q(i) }
# while gradient U(q) != 0 do
#   q(i+1) = q(i) + alpha(i)*gradient U (q(i))
#   i = i +1
# end while
def gradient_descent(start_state, goal_state, tolerance, att_pot, visualize):
    # Parameters
    zeta = 2.1
    i = 0
    alpha = 0.05
    # init variables
    q = np.array(start_state)
    gradient = q    # init random values
    q_list = [gradient]

    # Algorithm
    while np.linalg.norm(q_list[i]-goal_state, 2) > tolerance:
        if att_pot == "conic":
            gradient = ConicAttractivePotential(q_list[i], goal_state, zeta)
        elif att_pot == "quadratic":
            gradient = QuadraticAttractivePotential(q_list[i], goal_state, zeta)
        elif att_pot == "combine":
            gradient = CombAttractivePotential(q_list[i], goal_state, zeta)
        temp = q_list[i] - alpha*gradient
        print(f"U_att = {gradient}, \tnew_q = {temp},\tprev_q = {q_list[i]}")
        
        i = i+1
        q_list.append(temp)
        # time.sleep(0.5) # just so I am not overflown with print statements
    print(f"-------------\nIterations: {i}")

    # Visualization
    if visualize:
        # ------- Create plot --------
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel('q1')
        ax.set_ylabel('q2')
        
        plt.axis([-10, 10, -10, 10])
        plt.grid(True)
        plt.scatter(goal_state[0], goal_state[1], color='g')

        for q in q_list:
            plt.scatter(q[0], q[1])
            plt.pause(0.02)
        # ------- Visualize -------
        # plt.legend()
        plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=list, default=[-9, -8])
    parser.add_argument('--goal', type=list, default=[8, 6.1])
    parser.add_argument('--tolerance', type=float, default=1e-1)
    parser.add_argument('--att_pot', type=str, default = "conic")
    parser.add_argument('--visualize', type=bool, default = True)
    args = parser.parse_args()

    gradient_descent(args.start, args.goal, args.tolerance, args.att_pot, args.visualize)
