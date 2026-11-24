public class NodoABB {
    int dato;
    NodoABB izq, der;

    NodoABB(int dato) {
        this.dato = dato;
    }

    boolean esHoja() {
        return izq == null && der == null;
    }
}
