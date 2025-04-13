import matplotlib.pyplot as plt
import numpy as np
from qutip import Bloch
from matplotlib.table import table
#from bloch import blochanim

# 1. Classical Bits vs. Qubits
def plot_bits_vs_qubits():
    """Visualize a classical bit (0 or 1) vs. a qubit in superposition."""
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    
    # Classical Bit (e.g., 0)
    ax[0].bar([0, 1], [1, 0], color='blue')
    ax[0].set_title("Bit (1 ali 0)")
    ax[0].set_xticks([0, 1])
    ax[0].set_ylim(0, 1)
    
    # Qubit (e.g., superposition 0.6|0> + 0.8|1>)
    alpha, beta = 0.5, 0.5  # Example amplitudes (not normalized for simplicity)
    ax[1].bar([0, 1], [alpha, beta], color='green')
    ax[1].set_title("Qubit (npr. $|\psi>=0.5|0> + 0.5|1>$)")
    ax[1].set_xticks([0, 1])
    ax[1].set_ylim(0, 1)
    #plt.savefig("bvqb.png")
    plt.show()

# 2. Blochova kugla
def plot_bloch_sphere():
    """Plot a qubit state on the Bloch sphere using qutip."""
    b = Bloch()
    # Example state: |+> = (|0> + |1>)/sqrt(2), lies on the equator
    vectors =[
        [1, 0, 0],    # |+> state
        [.3, .5, .6],
        [.4, 0, .5],
        [-.3, -.6, .4],
        [-.6, .3, -.3]
    ]
    for v in vectors:
        b.add_vectors(vectors)
    #plt.savefig("BlochS.png")
    b.show()

# 3. Word Length in Bits and Qubits
def plot_word_length(word="timjavornik"):
    """Compare the bits and qubits needed to store a word."""
    num_chars = len(word)
    bits_per_char = 8  # ASCII uses 8 bits per character
    total_bits = num_chars * bits_per_char
    print(f"beseda: '{word}'")
    print(f"Število črk: {num_chars}")
    print(f"Vsota bitov: {total_bits}")
    print(f"Vsota qubitov: {total_bits} (Ali |0> ali |1>)")
    
    # Visualize the first character's bits and equivalent qubits
    first_char = word[0]
    ascii_val = ord(first_char)
    binary_str = bin(ascii_val)[2:].zfill(8)  # Convert to 8-bit binary
    print(f"Prva črka '{first_char}' V binarnem zapisu: {binary_str}")
    
    # Create a table-like plot
    fig, ax = plt.subplots()
    ax.axis('off')
    table_data = [
        ["Bit 0", binary_str[0], "|0>" if binary_str[0] == '0' else "|1>"],
        ["Bit 1", binary_str[1], "|0>" if binary_str[1] == '0' else "|1>"],
        ["Bit 2", binary_str[1], "|0>" if binary_str[1] == '0' else "|1>"],
        ["Bit 3", binary_str[1], "|0>" if binary_str[1] == '0' else "|1>"],
        ["Bit 4", binary_str[0], "|0>" if binary_str[0] == '0' else "|1>"],
        ["Bit 5", binary_str[1], "|0>" if binary_str[1] == '0' else "|1>"],
        ["Bit 6", binary_str[0], "|0>" if binary_str[0] == '0' else "|1>"],
        #["...", "...", "..."],
        ["Bit 7", binary_str[0], "|0>" if binary_str[0] == '0' else "|1>"]
    ]
    tbl = table(ax, cellText=table_data, colLabels=["$N$", "Bit", "Qubit"], loc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1, 1.5)
    plt.savefig("tablelett.png")
    plt.show()

# 4. Grover's Algorithm Visualization
def plot_grovers_algorithm():
    """Visualize amplitude amplification in Grover's algorithm for a 2-qubit system."""
    states = ['|00>', '|01>', '|10>', '|11>']
    initial_amplitudes = [0.5, 0.5, 0.5, 0.5]  # Equal superposition for 4 states
    after_oracle = [0.5, 0.5, 0.5, -0.5]  # Mark |11> as the target
    after_diffusion = [0, 0, 0, 1]  # Amplify |11> after diffusion
    
    fig, ax = plt.subplots(1, 5, figsize=(15, 4))
    
    ax[0].bar(states, initial_amplitudes)
    ax[0].axhline(y=0, color='red', linestyle='--')  # Add horizontal line
    ax[0].set_title("Začetna superpozicija")
    ax[0].set_ylim(-1, 1)

    # --- Oracle Step Visualization ---
    ax[1].bar(states, initial_amplitudes, alpha=0.3, label='Začetno stanje', color='blue')
    ax[1].bar(states, after_oracle, alpha=0.7, label='Black Box (BB)', color='red', edgecolor='black')
    ax[1].axhline(0, color='gray', linestyle='--')
    ax[1].set_title("BB: Označi tarčno stanje", fontsize=12)
    ax[1].annotate('Obrat faze (BB)', xy=(0, -0.2), xytext=(0, -0.2))
    ax[1].legend()
    
    ax[2].bar(states, after_oracle)
    ax[2].axhline(y=0, color='red', linestyle='--')  # Add horizontal line
    ax[2].set_title("Stanje po BB (označena tarča)")
    ax[2].set_ylim(-1, 1)

    # --- Diffusion Step Visualization ---
    ax[3].bar(states, after_oracle, alpha=0.3, label='Po BB', color='red')
    ax[3].bar(states, after_diffusion, alpha=0.7, label='Po difuziji', color='green', edgecolor='black')
    ax[3].axhline(0, color='gray', linestyle='--')
    ax[3].set_title("Difuzija: Amplifikacija tarčnega stanja", fontsize=12)
    
    # Add amplitude reflection explanation
    avg_amplitude = np.mean(after_oracle)
    ax[3].axhline(avg_amplitude, color='purple', linestyle=':', label='Povprečna amplituda')
    ax[3].annotate('Inverzija okrog povprečja', xy=(3, 1), xytext=(2, 1.2))
    ax[3].legend()
    
    ax[4].bar(states, after_diffusion)
    ax[4].axhline(y=0, color='red', linestyle='--')  # Add horizontal line
    ax[4].set_title("Po difuziji (Amplificirano stanje)")
    ax[4].set_ylim(-1, 1)
    
    plt.tight_layout()
    #plt.savefig("Grovers.png")
    plt.savefig("Grovers.svg")
    plt.show()

# 5. Shor's Algorithm Visualization
def plot_shors_algorithm():
    """Visualize period-finding in Shor's algorithm with a periodic function."""
    # Example: f(x) = 2^x mod 15, period r=4 (since 2^4 ≡ 1 mod 15)
    a, N, r = 2, 15, 4
    x = np.arange(0, 15)
    f_x = np.mod(a**x, N)  # Periodic function
    
    # Simulate QFT output: peaks at multiples of 2^n / r
    n = 4  # 4 qubits, 2^n = 16
    qft_output = np.zeros(16)
    for k in range(16):
        if k % (16 // r) == 0:
            qft_output[k] = 1  # Peaks indicate the period
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    
    ax[0].plot(x, f_x, 'o-')
    ax[0].set_title(f"Periodična Funkcija $f(x) = {a}^x mod {N}$, perioda $r={r}$")
    ax[0].set_xlabel("x")
    ax[0].set_ylabel("f(x)")
    
    ax[1].bar(range(16), qft_output)
    ax[1].set_title("Simulirana kvantna Furierova Transformacija (Vrhovi pri večkratnikih $2^n / r$)")
    ax[1].set_xlabel("Izmerjena vrednost")
    ax[1].set_ylabel("Verjetnost")
    
    #plt.savefig("Shors.png")
    plt.show()

def shors_2():
    n = 13  # Number of qubits in Register 1
    r = 5   # Period (example for N=15, a=7)
    s = 7   # Integer coprime to r

    k_values = np.arange(2**n)
    k = k_values*s/r
    prob = np.abs(np.sum([np.exp(2j * np.pi * x * (k - s * 2**n / r) / 2**n) 
                        for x in range(r)], axis=0) / r)**2

    plt.plot(k_values, prob)
    plt.xlabel('k')
    plt.ylabel('Probability')
    plt.title('QFT Output Peaks for Period r=5')
    plt.show()

# Main function to run all visualizations
def main():
    print("1. Bit vs. Qubit")
    #plot_bits_vs_qubits()
    
    print("\n2. Blochova Krogelna lupina kot qubit")
    #plot_bloch_sphere()
    
    print("\n3. Dolžina besede v bitih in qubitih")
    #plot_word_length()
    
    print("\n4. Vizualizacija Groverjevega algoritma")
    #plot_grovers_algorithm()
    
    print("\n5. Vizualizacija Shorovega algoritma")
    #plot_shors_algorithm()

    print("\n6. Shorov algoritem 2")
    shors_2()

if __name__ == "__main__":
    main()