from __future__ import print_function
import numpy as np
from scipy.sparse import lil_matrix
from scipy.special import expit


class ESN:
    def __init__(self,
                 reservoir_size=100,
                 inputs=2,
                 outputs=1,
                 generate_time_sequence=False,
                 input_to_output=True,
                 reservoir_connectivity=10,
                 simulation_steps=10,
                 echo_decay=0.8,
                 verbose=True):
        self.reservoir_size = reservoir_size
        self.inputs = inputs
        self.outputs = outputs
        self.generate_time_sequence = generate_time_sequence
        self.input_to_output = input_to_output
        self.reservoir_connectivity = reservoir_connectivity
        self.echo_decay = echo_decay
        self.simulation_steps = simulation_steps
        self.verbose = verbose

    def createNetwork(self):
        if self.verbose:
            print("INFO: starting allocating memory for network")

        self.N_reservoir = np.zeros(self.reservoir_size)
        self.N_input = np.zeros(self.inputs)
        self.N_output = np.zeros(self.outputs)

        self.W_reservoir = np.zeros((self.reservoir_size, self.reservoir_size))
        for row in range(self.reservoir_size):
            columns = np.arange(self.reservoir_size)
            np.random.shuffle(columns)
            randomColumns = columns[:self.reservoir_connectivity]
            for col in randomColumns:
                self.W_reservoir[row, col] = np.random.rand()

        self.W_inputs = np.zeros((self.inputs, self.reservoir_size))
        for row in range(self.inputs):
            columns = np.arange(self.reservoir_size)
            np.random.shuffle(columns)
            randomColumns = columns[:self.reservoir_connectivity]
            for col in randomColumns:
                self.W_inputs[row, col] = np.random.rand()

        # self.W_out = lil_matrix(self.outputs, self.reservoir_size+self.inputs)
        self.W_out = np.zeros((self.outputs, self.reservoir_size))

        if self.verbose:
            print("INFO: done allocating memory for network")

    def simulateStep(self):
        N_reservoir_tmp = self.N_reservoir
        N_output_tmp = self.N_output

        for i_res in range(self.reservoir_size):
            val_inputs = np.dot(self.N_input.T, self.W_inputs[:, i_res])
            val_res = np.dot(self.N_reservoir.T, self.W_reservoir[:, i_res])
            new_val = self.activation(val_inputs + val_res, self.N_reservoir[i_res])
            N_reservoir_tmp[i_res] = new_val

        self.N_reservoir = N_reservoir_tmp

        for i_out in range(self.outputs):
            val_res = np.dot(self.N_reservoir, self.W_out[i_out, :])
            N_output_tmp[i_out] = val_res

        self.N_output = N_output_tmp

    def activation(self, newInput, oldAct):
        return expit(self.echo_decay * oldAct + newInput)

    def _getTotalOutputLength(self, output):
        totalCount = 0
        for out in output:
            totalCount += len(out)
        # print("totalCount",totalCount)
        return totalCount

    def _progress(self, current, total):
        if self.verbose:
            percentDone = float(current) / total * 100
            print("INFO: simulation {:.2f}% done".format(percentDone), end='\r')

    def train(self, inputs, outputs):
        totalOutputLen = len(inputs)
        if self.generate_time_sequence:
            totalOutputLen = self._getTotalOutputLength(outputs)
        states = np.empty((totalOutputLen, self.reservoir_size))

        if self.verbose:
            print("INFO: starting training")

        counter = 0
        for i_in in range(len(inputs)):
            self.N_input = np.array(inputs[i_in])
            if self.generate_time_sequence:
                for i_out in range(len(outputs[i_in])):
                    for i_iter in range(self.simulation_steps):
                        self.simulateStep()
                    states[counter] = self.N_reservoir
                    counter += 1
                    self._progress(counter, totalOutputLen)
            else:
                for i_step in range(self.simulation_steps):
                    self.simulateStep()
                states[i_in] = self.N_reservoir
                counter += 1
                self._progress(counter, totalOutputLen)

        if self.verbose:
            print("INFO: done training, now calculating output weights")

        outputArr = np.vstack(outputs)
        w_out_tmp = np.linalg.lstsq(states, outputArr)
        self.W_out = np.atleast_2d(w_out_tmp[0]).T

        if self.verbose:
            print("INFO: done calculating output weights")

    def predict(self, inputs, steps=1):
        states = np.empty((len(inputs) * steps, self.outputs))

        if self.verbose:
            print("INFO: starting prediction")

        for i_in in range(len(inputs)):
            self.N_input = np.array(inputs[i_in])
            if self.generate_time_sequence:
                for i_out in range(steps):
                    for i_step in range(self.simulation_steps):
                        self.simulateStep()
                    states[i_in * steps + i_out] = self.N_output
            else:
                for i_step in range(self.simulation_steps):
                    self.simulateStep()
                states[i_in] = self.N_output

        return states


if __name__ == "__main__":
    esn = ESN(reservoir_size=20, reservoir_connectivity=3, outputs=1)
    esn.createNetwork()
    # print esn.W_reservoir
    esn.train([[1, 1], [0, 1], [1, 0], [0, 0]], [[1], [0], [0], [1]])
    print(esn.predict([[1, 1], [0, 1], [1, 0], [0, 0]]))
