import matplotlib.pyplot as plt
import numpy as np


def conv_to_ndarr(inputs):
    return map(lambda x:np.array(x), inputs)

# plot Te, Vp, alpha, ne
def plot_default(x, Te, Vp, alpha, ne, x_type, save=False):
    x, Te, Vp, alpha, ne = conv_to_ndarr((x, Te, Vp, alpha, ne))

    plt.subplots(figsize = (6,12))

    ax1 = plt.subplot(4,1,1)
    plt.plot(x, Te, 'o-r')
    plt.ylabel('Te [eV]', fontdict={'size':12})
    plt.grid(True)

    ax2 = plt.subplot(4,1,2, sharex = ax1)
    plt.plot(x, ne, 'o-c')
    plt.ylabel('ne [m-3]', fontdict={'size':12})
    plt.grid(True)

    ax3 = plt.subplot(4,1,3, sharex = ax1)
    plt.plot(x, Vp, 'o-b')
    plt.ylabel('Vp [V]', fontdict={'size':12})
    plt.grid(True)

    ax4 = plt.subplot(4,1,4, sharex = ax1)
    plt.plot(x, alpha, 'o-g')
    plt.ylabel('Eletronegativity', fontdict={'size':12})
    if x_type == 'Distance':
        plt.xlabel('Distance [mm]', fontdict={'size':12})
    elif x_type == 'B-field':
        plt.xlabel('B-field [G]', fontdict={'size':12})
    plt.grid(True)
    
    plt.subplots_adjust(left=0.125, bottom=0.1,  right=0.9, top=0.9, wspace=0.2, hspace=0.2)
    if save:
        plt.savefig('default.png')
    plt.show()

# plot nm, np & ne & ne, nm, np
def plot_density(x, ne, nm, x_type, save=False):
    x, ne, nm = conv_to_ndarr((x, ne, nm))

    plt.subplots(figsize = (6,12))
    
    ax1 = plt.subplot(3,1,1)
    plt.plot(x, nm, 'o-m', x,  nm + ne, 'o-k')
    plt.ylabel('Density [m-3]', fontdict={'size':12})
    plt.legend(['Negative ion', 'Positive ion'])
    plt.grid(True)

    ax2 = plt.subplot(3,1,2, sharex = ax1)
    plt.plot(x, ne, 'o-c')
    plt.ylabel('Density [m-3]', fontdict={'size':12})
    plt.legend(['Electron'])
    plt.grid(True)

    ax3 = plt.subplot(3,1,3, sharex = ax1)
    plt.plot(x, ne, 'o-c', x, nm, 'o-m', x, nm + ne, 'o-k')
    plt.ylabel('Density [m-3]', fontdict={'size':12})
    if x_type == 'Distance':
        plt.xlabel('Distance [mm]', fontdict={'size':12})
    elif x_type == 'B-field':
        plt.xlabel('B-field [G]', fontdict={'size':12})
    plt.legend(['Electron', 'Negative ion', 'Positive ion'])
    plt.grid(True)

    plt.subplots_adjust(left=0.125, bottom=0.1,  right=0.9, top=0.9, wspace=0.2, hspace=0.2)
    
    if save:
        plt.savefig('density.png')
    plt.show()

# plot EEPF, dIdV for checking
def plot_check(energy, eepf, V, dIdV, Vp, save=False):
    plt.subplots(figsize = (15,5))
    
    ax1 = plt.subplot(1,2,1)
    plt.plot(energy, eepf, '-m')
    plt.title('EEPF')
    plt.ylabel('EEPF', fontdict={'size':12})
    plt.yscale('log')
    plt.ylim(1e8, 1e16)
    plt.xlabel('Energy [eV]', fontdict={'size':12})
    plt.xlim(0,)
    plt.xticks(np.arange(0, 50, 2))
    plt.grid(True)

    ax2 = plt.subplot(1,2,2)
    plt.plot(V, dIdV, '-c')
    plt.title('dI/dV')
    plt.ylabel('dI/dV [A/V]', fontdict={'size':12})
    plt.xlabel('Voltage [V]', fontdict={'size':12})
    plt.xticks(np.arange(-40, 40, 4))
    plt.legend(['Vp = {:.4f}'.format(Vp)])
    plt.grid(True)

    
    if save:
        plt.savefig('eepf_dIdV.png')
    plt.show()