import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class CityDriver {

    public static void main(String[] args) {
        long start = System.nanoTime();
        cityFan10();
        cityFan200();
        long end = System.nanoTime();
        System.out.println("Total run time = " + ((end - start)/1000000000.0) + " seconds.");
    }

    public static void cityFan10(){

        List<CityBean> beans = buildCityBeans();
        writeLeafFiles("data/cities/fan10/", 7, beans);
        writeSecondLevelNodes("data/cities/fan10/",7,beans,10, 4);
        writeThirdLevel("data/cities/fan10/",beans,9);

        //write root
        PrintWriter pw = null;

        try {
            pw = new PrintWriter("data/cities/fan10/city_node_0");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        pw.write("city_node_1,Hinesville,city_node_2,San Jose,city_node_3");


    }

    public static void cityFan200(){
        List<CityBean> beans = buildCityBeans();
        writeLeafFiles("data/cities/fan200/", 180, beans);
        writeSecondLevelNodes("data/cities/fan200/", 180, beans,10, 0 );
    }

    public static List<CityBean> buildCityBeans(){
        Connection conn = DatabaseConnection.getConnection();
        PreparedStatement ps;
        ResultSet rs;
        List<CityBean> beans = new ArrayList<>();
        String query = "SELECT * FROM City";
        try {
            ps = conn.prepareStatement(query);
            rs = ps.executeQuery();
            while (rs.next()){
                beans.add(new CityBean(rs.getInt("id"),rs.getString("name")));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return beans;
    }

    public static void writeLeafFiles(String filenamePrefix, int numRecordsPerLeaf, List<CityBean> beans){
        PrintWriter pw = null;
        String pointer;
        int currentFileNum = 0;
        int currNumEntries = 0;
        try {
            pw = new PrintWriter(filenamePrefix + "city_leaf_" + currentFileNum++);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        pw.write("" + ",");
        for(int i = 0; i < beans.size(); i++){
            if(currNumEntries == numRecordsPerLeaf){
                pw.write("city_leaf_" + currentFileNum);
                pw.close();
                currNumEntries = 0;
                try {
                    pw = new PrintWriter(filenamePrefix + "city_leaf_" + currentFileNum++);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                pointer = "city_leaf_" + (currentFileNum - 2);
                pw.write(pointer + ",");
            }
            pw.write(beans.get(i).getName() + ";" + beans.get(i).getId() + ",");
            currNumEntries++;
        }
        pw.write("");
        pw.close();
    }

    public static void writeSecondLevelNodes(String filePrefix, int numEntriesPerLeafFile, List<CityBean> beans, int numEntriesPerNode, int nodeStartNum){
        PrintWriter pw = null;
        int currentNumValues = 0;
        int currPointerVal = 0;
        int currentNodeVal = nodeStartNum;
        int entriesSeenSinceWrite = 0;
        try {
            pw = new PrintWriter(filePrefix + "city_node_" + currentNodeVal++);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        for(int i = 0; i < beans.size(); i++){
            if(currentNumValues == numEntriesPerNode - 1 && entriesSeenSinceWrite == numEntriesPerLeafFile){
                i = i + numEntriesPerLeafFile;
                pw.write("city_leaf_" + currPointerVal++);
                pw.close();
                try {
                    pw = new PrintWriter(filePrefix + "city_node_" + currentNodeVal++);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                pw.write("city_leaf_" + currPointerVal++ + ",");
                pw.write(beans.get(i).getName() + ",");
                currentNumValues = 1;
                entriesSeenSinceWrite = 0;
            }
            else if(entriesSeenSinceWrite == numEntriesPerLeafFile){
                pw.write("city_leaf_" + currPointerVal++ + ",");
                pw.write(beans.get(i).getName() + ",");
                currentNumValues++;
                entriesSeenSinceWrite = 0;
            }
            entriesSeenSinceWrite++;
        }

        pw.write("city_leaf_" + currPointerVal++);
        pw.close();
    }

    public static void writeThirdLevel(String filePrefix, List<CityBean> beans, int numEntriesPerNode) {
        PrintWriter pw = null;
        int curPointerIndex = 4;
        int currNodeFile = 1;
        int currentEntries = 0;
        try {
            pw = new PrintWriter(filePrefix + "city_node_" + currNodeFile++);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        for(int i = 70; i < beans.size(); i = i + 70){
            if(currentEntries == numEntriesPerNode - 1){
                pw.write("city_node_" + curPointerIndex++);
                pw.close();
                try {
                    pw = new PrintWriter(filePrefix + "city_node_" + currNodeFile++);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                currentEntries = 0;
            }
            if(i > beans.size()){
                pw.write("city_node_" + curPointerIndex);
                pw.close();
                break;
            }
            pw.write("city_node_" + curPointerIndex++ + ",");
            pw.write(beans.get(i).getName() + ",");
            currentEntries++;
        }
        pw.close();
    }
}
