import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class TimeDriver{

    public static void main(String[] args) {
        long start = System.nanoTime();
        timeFan10();
        timeFan200();
        long end = System.nanoTime();
        System.out.println("Total run time = " + ((end - start)/1000000000.0) + " seconds.");
    }

    public static void timeFan10(){

        List<TimeBean> beans = buildTimeBeans();
        writeLeafFiles("data/times/fan10/", 9, beans);
        writeSecondLevelNodes("data/times/fan10/",9,beans,10);
        writeThirdLevel("data/times/fan10/",beans,10);

        //write root
        PrintWriter pw = null;

        try {
            pw = new PrintWriter("data/times/fan10/time_node_0");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        pw.write("time_node_1,15:00:00,time_node_2");
        pw.close();

    }

    public static void timeFan200(){
        List<TimeBean> beans = buildTimeBeans();
        writeLeafFiles("data/times/fan200/", 180, beans);
        PrintWriter pw = null;

        try {
            pw = new PrintWriter("data/times/fan200/time_node_0");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        pw.write("time_leaf_0,03:00:00,time_leaf_1,06:00:00,time_leaf_2,09:00:00,time_leaf_3,12:00:00,time_leaf_4," +
                "15:00:00,time_leaf_5,18:00:00,time_leaf_6,21:00:00,time_leaf_7");
        pw.close();
    }

    public static List<TimeBean> buildTimeBeans(){
        Connection conn = DatabaseConnection.getConnection();
        PreparedStatement ps;
        ResultSet rs;
        List<TimeBean> beans = new ArrayList<>();
        String query = "SELECT * FROM Time";
        try {
            ps = conn.prepareStatement(query);
            rs = ps.executeQuery();
            while (rs.next()){
                beans.add(new TimeBean(rs.getInt("id"),rs.getString("value")));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return beans;
    }

    public static void writeLeafFiles(String filenamePrefix, int numRecordsPerLeaf, List<TimeBean> beans){
        PrintWriter pw = null;
        String pointer;
        int currentFileNum = 0;
        int currNumEntries = 0;
        try {
            pw = new PrintWriter(filenamePrefix + "time_leaf_" + currentFileNum++);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        pw.write("" + ",");
        for(int i = 0; i < beans.size(); i++){
            if(currNumEntries == numRecordsPerLeaf){
                pw.write("time_leaf_" + currentFileNum);
                pw.close();
                currNumEntries = 0;
                try {
                    pw = new PrintWriter(filenamePrefix + "time_leaf_" + currentFileNum++);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                pointer = "time_leaf_" + (currentFileNum - 2);
                pw.write(pointer + ",");
            }
            pw.write(beans.get(i).getValue() + ";" + beans.get(i).getId() + ",");
            currNumEntries++;
        }
        pw.write("");
        pw.close();
    }

    public static void writeSecondLevelNodes(String filePrefix, int numEntriesPerLeafFile, List<TimeBean> beans, int fan){
        PrintWriter pw = null;
        int currentNumValues = 0;
        int currPointerVal = 0;
        int currentNodeVal = 3;
        int entriesSeenSinceWrite = 0;
        try {
            pw = new PrintWriter(filePrefix + "time_node_" + currentNodeVal++);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        for(int i = 0; i < beans.size(); i++){
            if(currentNumValues == fan - 1 && entriesSeenSinceWrite == numEntriesPerLeafFile){
                i = i + numEntriesPerLeafFile;
                pw.write("time_leaf_" + currPointerVal++);
                pw.close();
                try {
                    pw = new PrintWriter(filePrefix + "time_node_" + currentNodeVal++);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                pw.write("time_leaf_" + currPointerVal++ + ",");
                pw.write(beans.get(i).getValue() + ",");
                currentNumValues = 1;
                entriesSeenSinceWrite = 0;
            }
            else if(entriesSeenSinceWrite == numEntriesPerLeafFile){
                pw.write("time_leaf_" + currPointerVal++ + ",");
                pw.write(beans.get(i).getValue() + ",");
                currentNumValues++;
                entriesSeenSinceWrite = 0;
            }
            entriesSeenSinceWrite++;
        }

            pw.write("time_leaf_" + currPointerVal++);
            pw.close();
    }

    public static void writeThirdLevel(String filePrefix, List<TimeBean> beans, int fan) {
        PrintWriter pw = null;
        int curPointerIndex = 3;
        int currNodeFile = 1;
        int currentEntries = 0;
        try {
            pw = new PrintWriter(filePrefix + "time_node_" + currNodeFile++);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        for(int i = 90; i < beans.size(); i = i + 90){
            if(currentEntries == fan - 1){
                i = i + 90;
                pw.write("time_node_" + curPointerIndex++);
                pw.close();
                try {
                    pw = new PrintWriter(filePrefix + "time_node_" + currNodeFile++);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                currentEntries = 0;
            }
            if(i > beans.size()){
                pw.write("time_node_" + curPointerIndex);
                pw.close();
                break;
            }
            pw.write("time_node_" + curPointerIndex++ + ",");
            pw.write(beans.get(i).getValue() + ",");
            currentEntries++;
        }
        pw.write("time_leaf_" + curPointerIndex++);
        pw.close();
    }

}
