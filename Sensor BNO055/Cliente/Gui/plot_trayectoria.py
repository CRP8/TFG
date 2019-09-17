from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt



def grafica(x, y, z, tx, ty):
    plt.ioff()

    plt.figure()
    ax = plt.axes(projection='3d')

    # Datos de ejemplo
    zline = np.linspace(0, 15, 1000)
    xline = np.sin(zline)
    yline = np.cos(zline)
    ax.plot3D(xline, yline, zline, 'gray')
    

    #Datos reales
    #ax.plot3D(x, y, z, 'gray')

    ax.set_title('Reconstruccion de la trayectoria')

    ax.set_xlabel('Valores de x')
    ax.set_ylabel('Valores de y')
    ax.set_zlabel('Valores de z')
    plt.savefig('Trayectoria.png')

    plt.figure()
    

    #Datos de ejemplo
    #plt.plot((1,2,3), (1 ,2, 3))
    plt.plot(np.exp(np.linspace(0,3, 10)))

    #Datos reales
    #plt.plot(tx, ty)

    plt.xlabel('Tiempo s')
    plt.ylabel('Velocidad m/s')

    #plt.show()
    plt.savefig('velocidad.png')
