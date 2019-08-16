"""
Hello QCSYSer!

In this exercise, students will attempt to optimize the parameters of
a circuit without knowing the actual contents of the circuit. Through this
activity students wilL *hopefully* reinvent some primitive form of gradient
descent, and so understand intuitively how a gradient-based optimizer works.
This will also demonstrate the difficulty that 'black box optimizers' face
when dealing with quantum circuits - i.e. variance of trigonometric functions
that can be either very large or vanishing.
"""
import sys
from os import system
import numpy as np

from matplotlib import cm, colors

import sympy
import cirq
import qutip



def cost_function(state, truth):
    """Compute 1 - <state|truth> on `state`, a single-qubit wavefunction."""
    return 1 - np.abs(np.dot(state.conj(), truth))**2


def state_array_to_qobj(state):
    return (state[0]*qutip.basis(2,0) + state[1]*qutip.basis(2,1)).unit()


# def view_colormap(cmap):
#     """Plot a colormap with its grayscale equivalent"""
#     cmap = plt.cm.get_cmap(cmap)
#     colors = cmap(np.arange(cmap.N))
#     fig, ax = plt.subplots(1, figsize=(6, 2),
#                            subplot_kw=dict(xticks=[], yticks=[]))
#     ax.imshow([colors], extent=[0, 10, 0, 1])
#     plt.show()


def main():

    # set up initial circuit
    params = [1.2, 2.9, 0.1]
    symbols = [sympy.Symbol(f"x{i}") for i in range(1,4)]
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit.from_ops(
        cirq.Rx(np.pi/4)(q), cirq.Ry(symbols[0])(q),
        cirq.Rx(symbols[1])(q), cirq.Rz(symbols[2])(q))

    # initialize the current state and target state
    current_state = None
    truth = np.array([0.149 + 0.238j, -0.745 - 0.607j])
    truth = truth / np.linalg.norm(truth)
    current_loss = 1

    # Bloch sphere and color palette
    rdbu = cm.get_cmap('bwr', 100)
    b = qutip.Bloch()
    b.sphere_color = "#ffffff"
    b.point_color = [1]
    b.xlabel = [r'$|$+$x\rangle$','']
    b.ylabel = [r'$|$+$y\rangle$','']
    b.show() # HACK - cycle through a showing to generate `axes` member
    # cache points and their color
    points_cache = []
    colors_cache = []

    # main routine:
    system('clear')
    print("Welcome. Prepare to optimize a PQC.")
    print("\tRed colors mean you're approaching the optimum")
    print("\tBlue colors mean you're moving away from the optimum")

    # while np.abs(current_loss) > 1e-4:
    for k in range(3000):
        # 0) reset Bloch sphere and stage plotting of points cache
        # Plot current state as black, previous ones according to heatmap
        b.clear()
        b.vector_color = ["#000000"] + colors_cache

        # 1) Get user input for parameters
        print("Iteration {}".format(k + 1))
        print("Pick the parameters to try this iteration:")
        params = []
        i = 1
        while len(params) < 4:
            try:
                params.append(float(input("Enter value for x{}: ".format(i))))
                i += 1
            except ValueError:
                print("Invalid input. Enter parameters again")
                params = []
                i = 1
                continue
            except KeyboardInterrupt:
                sys.exit()
        # be sneaky and make one parameter do nothing
        params = params[:2] + [params[3]]
        # 2) Simulate the new state
        current_state = cirq.Simulator().simulate(
            circuit, param_resolver=dict(zip(symbols, params))).final_state

        # color the vector and new point based on how well we guessed
        current_loss = cost_function(current_state, truth)
        current_vec = state_array_to_qobj(current_state)
        b.add_states(current_vec)
        b.add_states(points_cache)
        print("Current loss: {} \n".format(current_loss))
        # qutip's garbage mpl interface prevents fig management with gca()
        b.show()
        # 3) stage points cache for _next_ iteration
        points_cache.append(current_vec)
        print(current_vec)
        colors_cache.append(colors.to_hex(rdbu(current_loss), keep_alpha=False))

if __name__ == "__main__":
    main()
