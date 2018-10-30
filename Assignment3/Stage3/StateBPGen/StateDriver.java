import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.*;

public class StateDriver {

    public static void main(String[] args) {

        List<StateBean> beans = getStates();
        buildFan10(beans);
        buildFan200(beans);
    }

    public static void buildFan10(List<StateBean> beans){
        writeLeafFiles("data/states/fan10/", 9, beans);

        PrintWriter pw = null;
        try {
            pw = new PrintWriter("data/states/fan10/state_node_0");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        pw.write("state_leaf_0,Florida,state_leaf_1,Louisiana,state_leaf_2,Nebraska,state_leaf_3," +
                "Oklahoma,state_leaf_4,Vermont,state_leaf_5");
        pw.close();
    }

    public static void buildFan200(List<StateBean> beans){
        writeLeafFiles("data/states/fan200/", 199, beans);
        PrintWriter pw = null;
        try {
            pw = new PrintWriter("data/states/fan200/state_node_0");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        pw.write("state_leaf_0,Y,");
        pw.close();
    }
    public static void writeLeafFiles(String filenamePrefix, int numRecordsPerLeaf, List<StateBean> beans){
        PrintWriter pw = null;
        String pointer = "";
        int currentFileNum = 0;
        int currNumEntries = 0;
        try {
            pw = new PrintWriter(filenamePrefix + "state_leaf_" + currentFileNum++);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        pw.write("" + ",");
        for(int i = 0; i < beans.size(); i++){
            if(currNumEntries == numRecordsPerLeaf){
                pw.write("state_leaf_" + currentFileNum);
                pw.close();
                currNumEntries = 0;
                try {
                    pw = new PrintWriter(filenamePrefix + "state_leaf_" + currentFileNum++);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                pointer = "state_leaf_" + (currentFileNum - 2);
                pw.write(pointer + ",");
            }
            pw.write(beans.get(i).getName() + ";" + beans.get(i).getId() + ",");
            currNumEntries++;
        }
        pw.write("");
        pw.close();
    }

    public static List<StateBean> getStates(){
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

        return stateBeanList;
    }

}
