public class Node {
    private String state;
    private Node parent;
    private int depth;
    private int cost;

    public Node(String state, Node parent) {
        this.state = state;
        this.parent = parent;
        this.depth = parent == null ? 0 : parent.getDepth() + 1;
    }

    public String getState() { return state; }
    public Node getParent() { return parent; }
    public int getDepth() { return depth; }
    public int getCost() { return cost; }
    public void setCost(int cost) { this.cost = cost; }
}