"""
File: solvenet.c
Author:	Xavier Molero
Date: November, 1999
Revision (C code):   December, 2001
Revision2 (C code):  November, 2012 (UGR, UCO: any visit ratios -> Central Server Model not assumed)
Revision3 (Python code):  February, 2022 (UGR, direct translation to Python with no code re-writing or optimization)

Solves mono-class networks of queues, open and closed.
Parameters of the program: see command line

The code is not optimized: priority has been given to clarity.

The program does not make any error checking.

Examples:
    solvenet 0 5.0 3 0.01 9 0.02 3 0.016 5
    solvenet 1 2 2 3 0.01 10 0.02 5 0.03 4

"""

import sys

OPEN = 0
CLOSED = 1
Kmax = 20
network_type = OPEN  # by default network_type = OPEN

K = 0  # number of service stations

# structures_initialization():
# all the following are average values
Rm = 0.0  # R0min
R0 = 0.0  # server response time
X0 = 0.0  # server throughput
Xm = 0.0  # X0max
N0 = 0.0  # number of jobs in the server
V = [0.0] * Kmax  # visit ratio
S = [0.0] * Kmax  # service time
D = [0.0] * Kmax  # service demand
U = [0.0] * Kmax  # utilization
X = [0.0] * Kmax  # throughput
R = [0.0] * Kmax  # response time
N = [0.0] * Kmax  # number of jobs in the service station
Q = [0.0] * Kmax  # number of jobs in queue
W = [0.0] * Kmax  # waiting time
Z = 0.0  # user's think time

basic_output = 0

NT = 0  # total number of jobs/users in a closed network
knee_point = 0.0  # knee point
imax = 0  # index of the first bottleneck device found


def input_arguments():
    global network_type
    global S, V, K
    global X0
    global NT, Z
    global basic_output

    validate_input_parameters()
    if sys.argv[1] == '1':
        network_type = CLOSED
        NT = int(sys.argv[2])
        Z = float(sys.argv[3])
        K = int(sys.argv[4])
        for i in range(K):
            S[i] = (float(sys.argv[2 * i + 5]))
            V[i] = (float(sys.argv[2 * i + 6]))
        if len(sys.argv) > 2 * K + 4 + 1:
            basic_output = 1  # more parameters than needed -> basic output
    else:  # by default network_type = OPEN
        network_type = OPEN
        X0 = float(sys.argv[2])
        K = int(sys.argv[3])
        for i in range(K):
            S[i] = (float(sys.argv[2 * i + 4]))
            V[i] = (float(sys.argv[2 * i + 5]))
        if len(sys.argv) > 2 * K + 3 + 1:
            basic_output = 1  # more parameters than needed -> basic output


def validate_input_parameters():
    if (len(sys.argv) < 2) or (sys.argv[1] not in ['0', '1']):
        print("ANALYSIS OF SIMPLE QUEUEING NETWORKS")
        print("by Xavier Molero. Version 2.2")
        print("************************************")
        print("Solver for simple queueing networks")
        print("")
        print("Usage: solvenet")
        print("Usage: solvenet [0|1] [lambda0| NT Z] K S1 V1...SK VK")
        print("\tWith no parameters, shows this message")
        print("\tnetwork: 0 (open) and 1 (closed)")
        print("\tlambda0: arrival rate = throughput (equilibrium assumed)(only for open networks)")
        print("\tNT:      total number of terminals/users/jobs in the network (only for closed networks)")
        print("\tZ:       think time (only interactive closed networks)")
        print("\tK:       number of service stations")
        print("\tSi:      service time of device i")
        print("\tVi:      ratio visit of device i")
        print("")
        exit(0)


def analysis_open_networks():
    global R0, N0, Rm
    for i in range(K):
        D[i] = V[i] * S[i]
        U[i] = X0 * D[i]
        X[i] = X0 * V[i]
        R[i] = S[i] / (1.0 - U[i])
        N[i] = U[i] / (1.0 - U[i])
        Q[i] = N[i] - U[i]
        W[i] = R[i] - S[i]

    for i in range(K):
        R0 = R0 + (R[i] * V[i])
        N0 = N0 + N[i]
        Rm = Rm + D[i]


def analysis_closed_networks():
    global Rm, R0, X0, N0
    for i in range(K):
        D[i] = S[i] * V[i]
        Rm = Rm + D[i]

    for n in range(1, NT + 1):
        for i in range(K):
            R[i] = S[i] * (1.0 + N[i])
        R0 = 0.0
        for i in range(K):
            R0 = R0 + (R[i] * V[i])
        X0 = n / (Z + R0)
        N0 = X0 * R0
        for i in range(K):
            N[i] = X0 * V[i] * R[i]
            X[i] = X0 * V[i]
            U[i] = X0 * V[i] * S[i]
            Q[i] = N[i] - U[i]
            W[i] = R[i] - S[i]


def analysis_asymptotic_limits():
    global Xm, knee_point, imax
    u_max = 0.0
    imax = 0
    for i in range(K):
        if U[i] >= u_max:
            u_max = U[i]
            imax = i
    Xm = 1.0 / D[imax]
    # if (Network_type == CLOSED) Na = (long) ceil((Rm+Z) / D[imax])
    if network_type == CLOSED:
        knee_point = (Rm + Z) / D[imax]


def output_results():
    if X0 >= Xm:
        print("\n\nThe arrival rate is too big for this server!!!! Quitting!\n")
        return
    if basic_output == 1:
        print(f"{NT}\t{N0:10.4f}\t{R0:10.4f}\t{X0:10.4f}")
        return

    print("ANALYSIS OF SIMPLE QUEUEING NETWORKS")
    print("by Xavier Molero. Version 2.1")
    print("************************************")
    print("\n")

    if network_type == OPEN:
        print("QUEUEING NETWORK: OPEN")
        print("Open Queueing Network Analysis Algorithm")
    else:
        print("QUEUEING NETWORK: CLOSED")
        print("Mean Value Analysis Algorithm")

    print("")

    print("*******************************************************************")
    print("*   NAME   *    Ui    *    Ni    *    Ri    *    Xi    *    Wi    *")
    print("*******************************************************************")
    print("*          *          *          *          *          *          *")
    for i in range(K):
        print(f"* DEV{i:2d}    *{U[i]:10.4f}*{N[i]:10.4f}*{R[i]:10.4f}*{X[i]:10.4f}*{W[i]:10.4f}*")

    print("*          *          *          *          *          *          *")

    print("*******************************************************************")
    print("")

    print("********************************************************")
    print("*   NAME   *    Vi    *     Si   *    Di    *    Qi    *")
    print("********************************************************")
    print("*          *          *          *          *          *")
    for i in range(K):
        print(f"* DEV{i:2d}    *{V[i]:10.4f}*{S[i]:10.4f}*{D[i]:10.4f}*{Q[i]:10.4f}*")
    print("*          *          *          *          *          *")

    print("********************************************************")
    print("")

    print("*******************************************")
    print("*         SYSTEM VARIABLES                *")
    print("*******************************************")
    print("*                              *          *")
    print(f"* #JOBS IN THE SYSTEM (N0)     *{N0:10.4f}*")
    if network_type == CLOSED:
        print(f"* #INTERACTIVE USERS (NZ)      *{float(NT - N0):10.4f}*")
        print(f"* #JOBS IN THE NETWORK (NT)    *{NT:10d}*")
        print(f"* KNEE POINT (NT*)             *{knee_point:10.4f}*")

    print("*                              *          *")
    print(f"* RESPONSE TIME (R0)           *{R0:10.4f}*")
    print(f"* MINIMUM RESPONSE TIME        *{Rm:10.4f}*")
    print("*                              *          *")
    print(f"* THROUGHPUT (X0)              *{X0:10.4f}*")
    print(f"* MAXIMUM THROUGHPUT           *{Xm:10.4f}*")
    print("*                              *          *")
    print("*******************************************")
    print("")

    print("****************************************")
    print("*         OPTIMISTIC BOUNDS            *")
    print("****************************************")
    print("*                                      *")
    if network_type == OPEN:
        print(f"* R0_min =  {Rm:10.4f}                 *")
        print(f"* X0_max =  {Xm:10.4f}                 *")
    else:
        print(f"* R0  <=   max {{{Rm:5.2f}, {D[imax]:5.2f}*NT-{Z:<5.2f}}} *")
        print(f"* X0  >=   min {{ NT/{Rm + Z:<5.2f}, {Xm:5.2f}}}      *")

    print("*                                      *")
    print("****************************************")
    print("")


def main():
    input_arguments()
    if network_type == OPEN:
        analysis_open_networks()
    else:
        analysis_closed_networks()
    analysis_asymptotic_limits()
    output_results()


if __name__ == "__main__":
    main()
