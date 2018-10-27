import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.*;

public class Driver {

    public static void main(String[] args) {

        //these first lines build the files for fan10
        Queue<StateBean[]> myQueue = enqueueStates();
        Queue<StateBean[]> myQueue2 = enqueueStates();
        List<String> nodeLeft = buildNode(myQueue, 6, 1);
        List<String> nodeRight = buildNode(myQueue, 5, 8);
        String[] root = {"1", "New York", "2"};
        buildFiles(myQueue2);
        buildNodeLevel(nodeLeft,nodeRight);
        buildRootFile(root);



        //remainder builds the files for fan200
        PrintWriter pw = null;
        Queue<StateBean[]> myQueue3 = enqueueStates();
        Queue<StateBean[]> myQueue4 = enqueueStates();
        int index = 0;
        String prevFile = "";
        String currFile;
        while (!myQueue3.isEmpty()) {
            StateBean[] beans = myQueue3.poll();
            for (StateBean b : beans) {
                currFile = "state_leaf_" + index++;
                if (b == null) {
                    pw.write("");
                    pw.close();
                    break;
                }
                try {
                    pw = new PrintWriter("data/states/fan200/" + currFile);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                pw.write(prevFile + ",");
                prevFile = currFile;
                String stateInfo = b.getId() + ":" + b.getName() + ",";
                pw.write(stateInfo);
                pw.write("state_leaf_" + index);
                pw.close();
            }
        }

            try {
                pw = new PrintWriter("data/states/fan200/state_node_0");
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
            int pointer = 0;
        boolean first = true;
            while (!myQueue4.isEmpty()){
                StateBean[] beans = myQueue4.poll();
                for(StateBean b : beans){
                    if(first){
                        first = false;
                        continue;
                    }
                    if(b==null){
                        pw.write("state_leaf_"+ pointer);
                        break;
                    }
                    else {
                        pw.write("state_leaf_"+ pointer++ + ",");
                        pw.write(b.getName() + ",");
                    }
                }
            }
            pw.close();


    }

    public static Queue<StateBean[]> enqueueStates(){
        Connection conn = DatabaseConnection.getConnection();
        PreparedStatement ps = null;
        ResultSet rs = null;
        String query = "SELECT * FROM State";
        List<StateBean> stateBeanList = new ArrayList<>();

        try {
            ps = conn.prepareStatement(query);
            rs = ps.executeQuery();

            while(rs.next()){
                stateBeanList.add(new StateBean(rs.getInt("id"),rs.getString("name")));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        Collections.sort(stateBeanList);
        int arraySize = 4;
        int index = 0;
        StateBean[] beans = new StateBean[arraySize];
        Queue<StateBean[]> myQueue = new LinkedList<>();
        for(StateBean b : stateBeanList){
            if(index == arraySize){
                myQueue.offer(beans);
                index = 0;
                beans = new StateBean[arraySize];
            }
            beans[index] = b;
            index++;
        }
        if(beans[0] != null){
            myQueue.offer(beans);
        }
        return myQueue;
    }

    public static List<String> buildNode(Queue<StateBean[]> myQueue, int nodeSize, int startPoint){
        List<String> node = new ArrayList<>();
        myQueue.poll();
        for(int i = 0; i < nodeSize; i++){
            StateBean[] beans = myQueue.poll();
            if(i == nodeSize-1){
                node.add("" + startPoint++);
                node.add(beans[0].getName());
                node.add("" + (startPoint));
            }
            else {
                node.add("" + startPoint++);
                node.add(beans[0].getName());
            }
        }
        return node;
    }

    public static void buildFiles(Queue<StateBean[]> myQueue){
        int currNum = 0;
        String prevFile = "";
        String currFile = "";
        while (!myQueue.isEmpty()){
            StateBean[] beans = myQueue.poll();
            PrintWriter pw = null;
            currFile = "data/states/fan10/state_leaf_" + currNum;
            try {
                pw = new PrintWriter(currFile);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
            pw.write(prevFile + ",");
            for(StateBean b: beans){
                if(b==null){
                    break;
                }
                String stateInfo = b.getId() + ":" + b.getName() + ",";
                pw.write(stateInfo);
            }
            if(myQueue.peek() == null){
                pw.write("");
            }
            else {
                pw.write("state_leaf_" + (currNum + 1));
            }
            prevFile = currFile;
            pw.close();
            currNum++;
        }
    }

    public static void buildNodeLevel(List<String> leftNode, List<String> rightNode){
        PrintWriter pw = null;
        int index = 0;
        int pointer = 0;
        try {
            pw = new PrintWriter("state_node_1");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        for(String s : leftNode){
            if(index % 2 != 0){
                pw.write(s + ",");
            }
            else {
                pw.write("state_leaf_"+ pointer++ + ",");
            }
            index++;
        }
        pw.close();
        index = 0;
        try {
            pw = new PrintWriter("data/states/fan10/state_node_2");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        for(String s : rightNode){
            if(index % 2 != 0){
                pw.write(s + ",");
            }
            else {
                pw.write("state_leaf_"+ pointer++ + ",");
            }
            index++;
        }
        pw.close();
    }

    public static void buildRootFile(String[] root){
        PrintWriter pw = null;
        try {
            pw = new PrintWriter("data/states/fan10/state_node_0");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        pw.write("state_node_1,New York,state_node_2");
        pw.close();
    }
}
