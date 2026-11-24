import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class ABB {
    private NodoABB raiz;
    private int tamanio;

    public boolean agregar(int dato) {
        NodoABB nuevo = new NodoABB(dato);
        if (raiz == null) {
            raiz = nuevo;
            tamanio++;
            return true;
        }
        NodoABB aux = raiz;
        while (true) {
            if (dato == aux.dato) return false;
            if (dato < aux.dato) {
                if (aux.izq == null) { aux.izq = nuevo; break; }
                aux = aux.izq;
            } else {
                if (aux.der == null) { aux.der = nuevo; break; }
                aux = aux.der;
            }
        }
        tamanio++;
        return true;
    }

    public boolean existe(int dato) {
        return existe(raiz, dato);
    }

    private boolean existe(NodoABB n, int dato) {
        if (n == null) return false;
        if (dato == n.dato) return true;
        return dato < n.dato ? existe(n.izq, dato) : existe(n.der, dato);
    }

    public boolean quitar(int dato) {
        if (!existe(dato)) return false;
        raiz = quitar(raiz, dato);
        tamanio--;
        return true;
    }

    private NodoABB quitar(NodoABB n, int dato) {
        if (dato < n.dato) {
            n.izq = quitar(n.izq, dato);
        } else if (dato > n.dato) {
            n.der = quitar(n.der, dato);
        } else {
            if (n.esHoja()) return null;
            if (n.izq == null) return n.der;
            if (n.der == null) return n.izq;
            // dos hijos: se sube el mayor del lado izquierdo (predecesor)
            NodoABB pred = n.izq;
            while (pred.der != null) pred = pred.der;
            n.dato = pred.dato;
            n.izq = quitar(n.izq, pred.dato);
        }
        return n;
    }

    public int profundidad() {
        return profundidad(raiz);
    }

    private int profundidad(NodoABB n) {
        return n == null ? -1 : 1 + Math.max(profundidad(n.izq), profundidad(n.der));
    }

    public int hojas() {
        return hojas(raiz);
    }

    private int hojas(NodoABB n) {
        if (n == null) return 0;
        if (n.esHoja()) return 1;
        return hojas(n.izq) + hojas(n.der);
    }

    public int getTamanio() {
        return tamanio;
    }

    public List<Integer> enOrden() {
        List<Integer> lista = new ArrayList<>();
        enOrden(raiz, lista);
        return lista;
    }

    private void enOrden(NodoABB n, List<Integer> lista) {
        if (n == null) return;
        enOrden(n.izq, lista);
        lista.add(n.dato);
        enOrden(n.der, lista);
    }

    public List<Integer> preOrden() {
        List<Integer> lista = new ArrayList<>();
        preOrden(raiz, lista);
        return lista;
    }

    private void preOrden(NodoABB n, List<Integer> lista) {
        if (n == null) return;
        lista.add(n.dato);
        preOrden(n.izq, lista);
        preOrden(n.der, lista);
    }

    public List<Integer> postOrden() {
        List<Integer> lista = new ArrayList<>();
        postOrden(raiz, lista);
        return lista;
    }

    private void postOrden(NodoABB n, List<Integer> lista) {
        if (n == null) return;
        postOrden(n.izq, lista);
        postOrden(n.der, lista);
        lista.add(n.dato);
    }

    // recorrido por niveles = busqueda primero en anchura
    public List<List<Integer>> porNiveles() {
        List<List<Integer>> niveles = new ArrayList<>();
        if (raiz == null) return niveles;
        Queue<NodoABB> cola = new LinkedList<>();
        cola.add(raiz);
        while (!cola.isEmpty()) {
            int cuantos = cola.size();
            List<Integer> nivel = new ArrayList<>();
            for (int i = 0; i < cuantos; i++) {
                NodoABB n = cola.poll();
                nivel.add(n.dato);
                if (n.izq != null) cola.add(n.izq);
                if (n.der != null) cola.add(n.der);
            }
            niveles.add(nivel);
        }
        return niveles;
    }

    public void dibujar() {
        if (raiz == null) {
            System.out.println("(arbol vacio)");
            return;
        }
        System.out.println(raiz.dato);
        dibujar(raiz.izq, "", raiz.der != null);
        dibujar(raiz.der, "", false);
    }

    private void dibujar(NodoABB n, String prefijo, boolean hayHermano) {
        if (n == null) return;
        System.out.println(prefijo + (hayHermano ? "|-- " : "\\-- ") + n.dato);
        String sig = prefijo + (hayHermano ? "|   " : "    ");
        dibujar(n.izq, sig, n.der != null);
        dibujar(n.der, sig, false);
    }
}
