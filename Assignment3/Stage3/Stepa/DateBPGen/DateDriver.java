import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class DateDriver {

    public static void main(String[] args) {
        long start = System.nanoTime();
        dateFan10();
        dateFan200();
        long end = System.nanoTime();
        System.out.println("Total run time = " + ((end - start)/1000000000.0) + " seconds.");
    }

    public static void dateFan10(){

        List<DateBean> beans = buildDateBeans();
        writeLeafFiles("data/dates/fan10/", 7, beans);
        writeSecondLevelNodes("data/dates/fan10/",7,beans,10, 1);

        //write root
        PrintWriter pw = null;

        try {
            pw = new PrintWriter("data/dates/fan10/date_node_0");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        pw.write("date_node_1,2013-03-15,date_node_2,2013-06-01,date_node_3,2013-08-15,date_node_4,2013-11-01,date_node_5");
        pw.close();

    }

    public static void dateFan200(){
        List<DateBean> beans = buildDateBeans();
        writeLeafFiles("data/dates/fan200/", 199, beans);
        writeSecondLevelNodes("data/dates/fan200/", 199, beans,10, 0 );
    }

    public static List<DateBean> buildDateBeans(){
        Connection conn = DatabaseConnection.getConnection();
        PreparedStatement ps;
        ResultSet rs;
        List<DateBean> beans = new ArrayList<>();
        String query = "SELECT * FROM Date";
        try {
            ps = conn.prepareStatement(query);
            rs = ps.executeQuery();
            while (rs.next()){
                beans.add(new DateBean(rs.getInt("id"),rs.getString("value")));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return beans;
    }

    public static void writeLeafFiles(String filenamePrefix, int numRecordsPerLeaf, List<DateBean> beans){
        PrintWriter pw = null;
        String pointer;
        int currentFileNum = 0;
        int currNumEntries = 0;
        try {
            pw = new PrintWriter(filenamePrefix + "date_leaf_" + currentFileNum++);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        pw.write("" + ",");
        for(int i = 0; i < beans.size(); i++){
            if(currNumEntries == numRecordsPerLeaf){
                pw.write("date_leaf_" + currentFileNum);
                pw.close();
                currNumEntries = 0;
                try {
                    pw = new PrintWriter(filenamePrefix + "date_leaf_" + currentFileNum++);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                pointer = "date_leaf_" + (currentFileNum - 2);
                pw.write(pointer + ",");
            }
            pw.write(beans.get(i).getValue() + ";" + beans.get(i).getId() + ",");
            currNumEntries++;
        }
        pw.write("");
        pw.close();
    }

    public static void writeSecondLevelNodes(String filePrefix, int numEntriesPerLeafFile, List<DateBean> beans, int numEntriesPerNode, int nodeStartNum){
        PrintWriter pw = null;
        int currentNumValues = 0;
        int currPointerVal = 0;
        int currentNodeVal = nodeStartNum;
        int entriesSeenSinceWrite = 0;
        try {
            pw = new PrintWriter(filePrefix + "date_node_" + currentNodeVal++);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        for(int i = 0; i < beans.size(); i++){
            if(currentNumValues == numEntriesPerNode - 1 && entriesSeenSinceWrite == numEntriesPerLeafFile){
                i = i + numEntriesPerLeafFile;
                pw.write("date_leaf_" + currPointerVal++);
                pw.close();
                try {
                    pw = new PrintWriter(filePrefix + "date_node_" + currentNodeVal++);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                pw.write("date_leaf_" + currPointerVal++ + ",");
                pw.write(beans.get(i).getValue() + ",");
                currentNumValues = 1;
                entriesSeenSinceWrite = 0;
            }
            else if(entriesSeenSinceWrite == numEntriesPerLeafFile){
                pw.write("date_leaf_" + currPointerVal++ + ",");
                pw.write(beans.get(i).getValue() + ",");
                currentNumValues++;
                entriesSeenSinceWrite = 0;
            }
            entriesSeenSinceWrite++;
        }

        pw.write("date_leaf_" + currPointerVal++);
        pw.close();
    }
}
