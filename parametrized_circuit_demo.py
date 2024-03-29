import sys
import numpy as np

from matplotlib import cm, colors

import sympy
import cirq
import qutip



def cost_function(state, truth):
    """Compute 1 - <state|truth> on `state`, a single-qubit wavefunction."""
    return np.abs(np.dot(state.conj(), truth))**2


def state_array_to_qobj(state):
    return (state[0]*qutip.basis(2,0) + state[1]*qutip.basis(2,1)).unit()


def main():

    circuit = cirq.Circuit.from_ops(cirq.Rx(sympy.Symbol("x"))(cirq.LineQubit(0)))

    # initialize the current state and target state
    current_state = None
    truth = np.array([1, 0])
    current_loss = 1

    # Bloch sphere and color palette
    rdbu = cm.get_cmap('coolwarm', 100)
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
    print("Welcome. Prepare to optimize a PQC.")
    print("\tBlue colors mean you're approaching the optimum")
    print("\tRed colors mean you're moving away from the optimum")
    for k in range(30):
        # 0) reset Bloch sphere and stage plotting of points cache
        # Plot current state as black, previous ones according to heatmap
        b.clear()
        b.vector_color = ["#000000"] + colors_cache

        # 1) Get user input for parameters
        print("Iteration {}".format(k + 1))
        print("Pick the parameters to try this iteration:")
        x = None
        while x is None:
            try:
                x = float(input("Enter value for x: "))
            except ValueError:
                print("Invalid input. Enter parameters again")
                x = None
                continue
            except KeyboardInterrupt:
                sys.exit()

        # 2) Simulate the new state
        current_state = cirq.Simulator().simulate(
            circuit, param_resolver={sympy.Symbol("x"): x}).final_state

        # color the vector and new point based on how well we guessed
        current_loss = cost_function(current_state, truth)
        current_vec = state_array_to_qobj(current_state)
        b.add_states(current_vec)
        b.add_states(points_cache)
        print("Current loss: {}".format(current_loss))
        b.show()

        # 3) stage points cache for _next_ iteration
        points_cache.append(current_vec)
        colors_cache.append(colors.to_hex(rdbu(current_loss), keep_alpha=False))

if __name__ == "__main__":
    main()
