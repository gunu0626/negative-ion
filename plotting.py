import matplotlib.pyplot as plt

#Te, Vp, alpha, ne plot
def plot_default(x, Te, Vp, alpha, ne):
    plt.subplots(figsize = (6,12))
    
    ax1 = plt.subplot(4,1,1)
    plt.plot(x, Te, 'o-r')
    plt.ylabel('Te [eV]', fontdict={'size':12})
    plt.grid(True)

    ax2 = plt.subplot(4,1,2, sharex = ax1)
    plt.plot(x, Vp, 'o-b')
    plt.ylabel('Vp [V]', fontdict={'size':12})
    plt.grid(True)

    ax3 = plt.subplot(4,1,3, sharex = ax1)
    plt.plot(x, alpha, 'o-g')
    plt.ylabel('Eletronegativity', fontdict={'size':12})
    plt.grid(True)

    ax4 = plt.subplot(4,1,4, sharex = ax1)
    plt.plot(x, ne, 'o-c')
    plt.ylabel('ne [m-3]', fontdict={'size':12})
    plt.xlabel('Distance [mm] or B-field [G]', fontdict={'size':12})
    plt.grid(True)
    
    plt.subplots_adjust(left=0.125, bottom=0.1,  right=0.9, top=0.9, wspace=0.2, hspace=0.2)
    plt.show()

#nm, np & ne & ne, nm, np plot
def plot_density(x, ne, nm, np):
    plt.subplots(figsize = (6,12))
    
    ax1 = plt.subplot(3,1,1)
    plt.plot(x, nm, 'o-m', x, np, 'o-k')
    plt.ylabel('Density [m-3]', fontdict={'size':12})
    plt.legend(['Negative ion', 'Positive ion'])
    plt.grid(True)

    ax2 = plt.subplot(3,1,2, sharex = ax1)
    plt.plot(x, ne, 'o-c')
    plt.ylabel('Density [m-3]', fontdict={'size':12})
    plt.legend(['Electron'])
    plt.grid(True)

    ax3 = plt.subplot(3,1,3, sharex = ax1)
    plt.plot(x, ne, 'o-c', x, nm, 'o-m', x, np, 'o-k')
    plt.ylabel('Density [m-3]', fontdict={'size':12})
    plt.xlabel('Distance [mm] or B-field [G]', fontdict={'size':12})
    plt.legend(['Electron', 'Negative ion', 'Positive ion'])
    plt.grid(True)

    plt.subplots_adjust(left=0.125, bottom=0.1,  right=0.9, top=0.9, wspace=0.2, hspace=0.2)
    plt.show()




