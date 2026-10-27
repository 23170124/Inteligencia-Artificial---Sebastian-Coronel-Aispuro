public class App {
    public static void main(String[] args) {
        // Estado inicial y estado meta del 8-puzzle (el 0 es el espacio vacio)
        String initialState = "123405678";
        String goalState = "123456780";
        SearchTree tree = new SearchTree(initialState, goalState);

        System.out.println("===== ANCHURA =====");
        tree.breadthFirstSearch();
        System.out.println("===== PROFUNDIDAD =====");
        tree.depthFirstSearch();
        System.out.println("===== COSTO UNIFORME =====");
        tree.UniformCostSearch();
        System.out.println("===== PROFUNDIDAD LIMITADA (limite 20) =====");
        tree.depthLimitedSearch(20);
        System.out.println("===== PROFUNDIDAD ITERATIVA =====");
        tree.iterativeDeepeningSearch(30);
        System.out.println("===== BIDIRECCIONAL =====");
        tree.bidirectionalSearch();

        // Al final se comparan todas las busquedas
        tree.comparisonTable(30);
    }
}