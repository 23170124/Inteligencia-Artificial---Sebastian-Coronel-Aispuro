import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.Set;


public class SearchTree {
    Node root;
    String initialState;
    String goalState;

    
    int lastTime;
    int lastVisited;
    int lastFrontier;
    int lastDepth;
    boolean lastFound;


    boolean showPath = true;

    
    int dlsTime;
    int dlsVisited;

    public SearchTree(String initialState, String goalState){
        this.initialState = initialState;
        this.goalState = goalState;
        this.root = new Node(initialState, null);
    }

    // 1. BUSQUEDA EN ANCHURA 
    public void breadthFirstSearch() {
        int time = 0;
       
        Set<String> visited = new HashSet<String>();
     
        Node currentNode = root;
        Queue<Node> queue = new LinkedList<>();
        queue.add(currentNode);
     
        while (!queue.isEmpty()) {
            time++;
         
            currentNode = queue.poll();
            visited.add(currentNode.getState());
            if(currentNode.getState().equals(goalState)) {
                showResults(currentNode, time, visited.size(), queue.size());
                return;
            }
            
            List<Node> children = NodeUtils.generateChildren(currentNode);
            for (Node child : children) {
                if (!visited.contains(child.getState()))
                    queue.add(child);
            }
        }
        showNotFound(time, visited.size());
    }

    // 2. BUSQUEDA EN PROFUNDIDAD 
    public void depthFirstSearch(){
        int time = 0;
        Set<String> visited = new HashSet<String>();
        
        Node currentNode = root;
        Deque<Node> stack = new LinkedList<>();
        stack.push(currentNode);
        while (!stack.isEmpty()) {
            time ++;
          
            currentNode = stack.pop();
            visited.add(currentNode.getState());
            if(currentNode.getState().equals(goalState)) {
                showResults(currentNode, time, visited.size(), stack.size());
                return;
            }

            List<Node> children = NodeUtils.generateChildren(currentNode);
            for (Node child : children) {
                if (!visited.contains(child.getState()))
                    stack.push(child);
            }
        }
        showNotFound(time, visited.size());
    }

    // 3. BUSQUEDA DE COSTO UNIFORME 
    public void UniformCostSearch() {
        int time = 0;
        Set<String> visited = new HashSet<String>();
        Node currentNode = root;
        
        PriorityQueue<Node> queue = new PriorityQueue<>(new NodePriorityComparator());
        queue.add(currentNode);
        while (!queue.isEmpty()) {
            time++;
            currentNode = queue.poll();

            if (visited.contains(currentNode.getState())) {
                continue;
            }
            visited.add(currentNode.getState());
            if(currentNode.getState().equals(goalState)) {
                showResults(currentNode, time, visited.size(), queue.size());
                return;
            }
            List<Node> children = NodeUtils.generateChildren(currentNode);
            for (Node child : children) {
                if (!visited.contains(child.getState())){
                    child.setCost(currentNode.getCost() + 1);
                    queue.add(child);
                }
            }
        }
        showNotFound(time, visited.size());
    }

    // 4. PROFUNDIDAD LIMITADA 
    public void depthLimitedSearch(int limit) {
        dlsTime = 0;
        dlsVisited = 0;
        Node result = limitedSearch(limit);
        if (result != null) {
            showResults(result, dlsTime, dlsVisited, 0);
        } else {
            showNotFound(dlsTime, dlsVisited);
        }
    }


    private Node limitedSearch(int limit) {
        
        Map<String, Integer> visited = new HashMap<>();
        Deque<Node> stack = new LinkedList<>();
        stack.push(root);
        while (!stack.isEmpty()) {
            dlsTime++;
            Node currentNode = stack.pop();
            visited.put(currentNode.getState(), currentNode.getDepth());
            if (currentNode.getState().equals(goalState)) {
                dlsVisited += visited.size();
                return currentNode;
            }
            
            if (currentNode.getDepth() < limit) {
                List<Node> children = NodeUtils.generateChildren(currentNode);
                for (Node child : children) {
                    if (!visited.containsKey(child.getState()) || child.getDepth() < visited.get(child.getState())) {
                        stack.push(child);
                    }
                }
            }
        }
        dlsVisited += visited.size();
        return null;
    }

    // 4. PROFUNDIDAD ITERATIVA 
    public void iterativeDeepeningSearch(int maxDepth) {
        dlsTime = 0;
        dlsVisited = 0;
        for (int limit = 0; limit <= maxDepth; limit++) {
            Node result = limitedSearch(limit);
            if (result != null) {
                System.out.println("Encontrado con limite: " + limit);
                showResults(result, dlsTime, dlsVisited, 0);
                return;
            }
        }
        showNotFound(dlsTime, dlsVisited);
    }

    //  5. BUSQUEDA BIDIRECCIONAL
    public void bidirectionalSearch() {
        int time = 0;
       
        Map<String, Node> visitedStart = new HashMap<>();
        Map<String, Node> visitedGoal = new HashMap<>();
        Queue<Node> queueStart = new LinkedList<>();
        Queue<Node> queueGoal = new LinkedList<>();

        Node goalNode = new Node(goalState, null);
        queueStart.add(root);
        queueGoal.add(goalNode);
        visitedStart.put(initialState, root);
        visitedGoal.put(goalState, goalNode);

       
        if (initialState.equals(goalState)) {
            showResults(root, 1, 1, 0);
            return;
        }

        while (!queueStart.isEmpty() && !queueGoal.isEmpty()) {
            
            time++;
            Node current = queueStart.poll();
            List<Node> children = NodeUtils.generateChildren(current);
            for (Node child : children) {
                if (!visitedStart.containsKey(child.getState())) {
                    visitedStart.put(child.getState(), child);
                    if (visitedGoal.containsKey(child.getState())) {
                        Node fromGoal = visitedGoal.get(child.getState());
                        showBidirectional(child, fromGoal, time, visitedStart.size() + visitedGoal.size(), queueStart.size() + queueGoal.size());
                        return;
                    }
                    queueStart.add(child);
                }
            }

            time++;
            current = queueGoal.poll();
            children = NodeUtils.generateChildren(current);
            for (Node child : children) {
                if (!visitedGoal.containsKey(child.getState())) {
                    visitedGoal.put(child.getState(), child);
                    if (visitedStart.containsKey(child.getState())) {
                        Node fromStart = visitedStart.get(child.getState());
                        showBidirectional(fromStart, child, time, visitedStart.size() + visitedGoal.size(), queueStart.size() + queueGoal.size());
                        return;
                    }
                    queueGoal.add(child);
                }
            }
        }
        showNotFound(time, visitedStart.size() + visitedGoal.size());
    }

    private void showBidirectional(Node fromStart, Node fromGoal, int time, int visited, int frontier) {
        System.out.println("Goal state found: " + goalState);
        if (showPath) {
            printPath(fromStart);
            Node n = fromGoal.getParent();
            while (n != null) {
                System.out.println(NodeUtils.formatState(n.getState()));
                n = n.getParent();
            }
        }
        int depth = fromStart.getDepth() + fromGoal.getDepth();
        printStats(time, visited, frontier, depth);
    }

    // 6. TABLA COMPARATIVA 
    public void comparisonTable(int maxDepth) {
        showPath = false;
        String[] names = {"Anchura", "Profundidad", "Costo uniforme", "Prof. limitada", "Prof. iterativa", "Bidireccional"};
        String[] timeComplexity = {"O(b^d)", "O(b^m)", "O(b^(C*/e))", "O(b^l)", "O(b^d)", "O(b^(d/2))"};
        String[] spaceComplexity = {"O(b^d)", "O(b*m)", "O(b^(C*/e))", "O(b*l)", "O(b*d)", "O(b^(d/2))"};
        String[] complete = {"Si", "No", "Si", "No", "Si", "Si"};
        String[] optimal = {"Si", "No", "Si", "No", "Si", "Si"};

        int[] expanded = new int[6];
        int[] visited = new int[6];
        int[] frontier = new int[6];
        int[] depth = new int[6];
        long[] millis = new long[6];

        for (int i = 0; i < 6; i++) {
            long start = System.currentTimeMillis();
            if (i == 0) breadthFirstSearch();
            if (i == 1) depthFirstSearch();
            if (i == 2) UniformCostSearch();
            if (i == 3) depthLimitedSearch(maxDepth);
            if (i == 4) iterativeDeepeningSearch(maxDepth);
            if (i == 5) bidirectionalSearch();
            millis[i] = System.currentTimeMillis() - start;

            expanded[i] = lastTime;
            visited[i] = lastVisited;
            frontier[i] = lastFrontier;
            depth[i] = lastDepth;
        }
        showPath = true;

        System.out.println();
        System.out.println("==================== TABLA COMPARATIVA ====================");
        System.out.printf("%-16s %-12s %-12s %-9s %-7s %-10s %-10s %-9s %-10s %-5s%n",
                "Algoritmo", "Tiempo", "Espacio", "Completa", "Optima", "Expandidos", "Visitados", "Frontera", "Solucion", "ms");
        for (int i = 0; i < 6; i++) {
            System.out.printf("%-16s %-12s %-12s %-9s %-7s %-10d %-10d %-9d %-10d %-5d%n",
                    names[i], timeComplexity[i], spaceComplexity[i], complete[i], optimal[i],
                    expanded[i], visited[i], frontier[i], depth[i], millis[i]);
        }
        System.out.println("b = factor de ramificacion, d = profundidad de la solucion, m = profundidad maxima");
        System.out.println("l = limite, C* = costo de la solucion optima, e = costo minimo de un paso");
    }

    //  METODOS PARA IMPRIMIR 

    private void printPath(Node node){
        Deque<Node> path = new LinkedList<>();
        while (node != null) {
            path.push(node);
            node = node.getParent();
        }
        for (Node n : path) {
            System.out.println(NodeUtils.formatState(n.getState()));
        }
    }

    private void showResults(Node goal, int time, int visited, int frontier) {
        System.out.println("Goal state found: " + goal.getState());
        if (showPath) {
            printPath(goal);
        }
        printStats(time, visited, frontier, goal.getDepth());
    }

    private void printStats(int time, int visited, int frontier, int depth) {
        System.out.println("time: " + time);
        System.out.println("Estados visitados: " + visited);
        System.out.println("Frontera: " + frontier);
        System.out.println("Profundidad de la solucion: " + depth);
        lastTime = time;
        lastVisited = visited;
        lastFrontier = frontier;
        lastDepth = depth;
        lastFound = true;
    }

    private void showNotFound(int time, int visited) {
        System.out.println("No se encontro el estado meta");
        System.out.println("time: " + time);
        System.out.println("Estados visitados: " + visited);
        lastTime = time;
        lastVisited = visited;
        lastFrontier = 0;
        lastDepth = -1;
        lastFound = false;
    }
}