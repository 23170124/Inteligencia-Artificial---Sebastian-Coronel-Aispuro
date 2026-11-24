import java.util.Scanner;

public class App {
    public static void main(String[] args) {
        ABB arbol = new ABB();
        Scanner sc = new Scanner(System.in);

        for (int x : new int[]{45, 23, 67, 12, 34, 56, 89, 29, 61}) {
            arbol.agregar(x);
        }

        int op;
        do {
            System.out.println("\n===== ARBOL BINARIO DE BUSQUEDA =====");
            System.out.println("1. Agregar");
            System.out.println("2. Buscar");
            System.out.println("3. Eliminar");
            System.out.println("4. Mostrar recorridos");
            System.out.println("5. Dibujar arbol");
            System.out.println("6. Estadisticas");
            System.out.println("0. Salir");
            System.out.print("Opcion: ");
            op = sc.nextInt();

            switch (op) {
                case 1 -> {
                    System.out.print("Valor: ");
                    int v = sc.nextInt();
                    System.out.println(arbol.agregar(v) ? "Agregado" : "Ya existe, no se agrego");
                }
                case 2 -> {
                    System.out.print("Valor: ");
                    int v = sc.nextInt();
                    System.out.println(arbol.existe(v) ? "Si esta en el arbol" : "No esta en el arbol");
                }
                case 3 -> {
                    System.out.print("Valor: ");
                    int v = sc.nextInt();
                    System.out.println(arbol.quitar(v) ? "Eliminado" : "No existe");
                }
                case 4 -> {
                    System.out.println("InOrden:    " + arbol.enOrden());
                    System.out.println("PreOrden:   " + arbol.preOrden());
                    System.out.println("PostOrden:  " + arbol.postOrden());
                    System.out.println("Por nivel:  " + arbol.porNiveles());
                }
                case 5 -> arbol.dibujar();
                case 6 -> {
                    System.out.println("Nodos:       " + arbol.getTamanio());
                    System.out.println("Hojas:       " + arbol.hojas());
                    System.out.println("Profundidad: " + arbol.profundidad());
                }
                case 0 -> System.out.println("Fin");
                default -> System.out.println("Opcion invalida");
            }
        } while (op != 0);

        sc.close();
    }
}
