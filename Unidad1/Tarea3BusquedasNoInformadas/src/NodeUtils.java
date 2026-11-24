import java.util.ArrayList;
import java.util.List;

public class NodeUtils {
    private static final int[][] MOVES = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

    public static List<Node> generateChildren(Node node) {
        List<Node> children = new ArrayList<>();
        String s = node.getState();
        int zero = s.indexOf('0');
        int r = zero / 3, c = zero % 3;
        for (int[] m : MOVES) {
            int nr = r + m[0], nc = c + m[1];
            if (nr < 0 || nr > 2 || nc < 0 || nc > 2) continue;
            char[] chars = s.toCharArray();
            int target = nr * 3 + nc;
            chars[zero] = chars[target];
            chars[target] = '0';
            children.add(new Node(new String(chars), node));
        }
        return children;
    }

    public static String formatState(String s) {
        return s.substring(0, 3) + "\n" + s.substring(3, 6) + "\n" + s.substring(6, 9) + "\n";
    }
}