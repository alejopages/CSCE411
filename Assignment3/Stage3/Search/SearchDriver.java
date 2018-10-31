import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class SearchDriver {

    public static void main(String[] args) {
        System.out.println(numPeopleFromNebraska(10));
        System.out.println(numPeopleWithMessageBetween("08:00:00", "09:00:00", 10));
        System.out.println(numPeopleFromNebraska(200));
        System.out.println(numPeopleWithMessageBetween("08:00:00", "09:00:00", 200));
    }

    public static int numPeopleFromNebraska(int fan){
        return findStateID("Nebraska", fan);
    }

    public static int numPeopleWithMessageBetween(String start, String end, int fan){

        List<Integer> result = findTimeIDs(start, end, fan);
        return result.size();
    }

    public static int findStateID(String state, int fan){

        String nextFile = searchNodeFile("data/states/fan" + fan + "/state_node_0", state);
        while(nextFile.contains("state_node")){
            nextFile = searchNodeFile("data/states/fan" + fan + "/" + nextFile, state);
        }
        int result = searchLeafFileSingleValue("data/states/fan" + fan + "/" + nextFile, state);
        return result;
    }

    public static List<Integer> findTimeIDs(String start, String end, int fan){
        String nextFile = searchNodeFile("data/times/fan" + fan + "/time_node_0", start);
        while(nextFile.contains("time_node")){
            nextFile = searchNodeFile("data/times/fan" + fan + "/" + nextFile, start);
        }
        List<Integer> result = searchLeafFileRange("data/times/fan" + fan + "/" + nextFile, start, end);
        return result;
    }

    public static String searchNodeFile(String file, String searchValue){
        BufferedReader br = null;
        String result = null;
        try {
            br = new BufferedReader(new FileReader(file));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        try {
            String[] data = br.readLine().split(",");

            for(int i = 1; i < data.length; i++){
                int compare = searchValue.compareTo(data[i]);
                if(i%2 != 0 && compare <= 0) {
                    if(compare < 0){
                        result = data[i - 1];
                    }
                    else {
                        result = data[i + 1];
                    }
                    break;
                }
                if(i == data.length - 2){
                    result = data[i + 1];
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return result;
    }

    public static int searchLeafFileSingleValue(String file, String searchValue){
        BufferedReader br = null;
        int result = -1;
        try {
            br = new BufferedReader(new FileReader(file));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        try {
            String[] data = br.readLine().split(",");
            result = binarySearch(searchValue, 1, data.length - 2, data);
            String[] vals = data[result].split(";");
            result = Integer.parseInt(vals[1]);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return result;
    }

    public static List<Integer> searchLeafFileRange(String file, String start, String end){
        BufferedReader br = null;
        List<Integer> results = new ArrayList<>();
        try {
            br = new BufferedReader(new FileReader(file));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        try {
            String[] data = br.readLine().split(",");
            int currIndex = binarySearch(start, 1, data.length - 2, data);
            while(data[currIndex].compareTo(end) <= 0){
                String[] time = data[currIndex].split(";");
                results.add(Integer.parseInt(time[1]));
                currIndex++;
                if(currIndex == data.length-1){
                    String[] fileName = file.split("/");
                    file = fileName[0] + "/" + fileName[1] + "/" + fileName[2] + "/" + data[currIndex];
                    br = new BufferedReader(new FileReader(file));
                    data = br.readLine().split(",");
                    currIndex = 1;
                }
                if(data[currIndex].contains(end)){
                    time = data[currIndex].split(";");
                    results.add(Integer.parseInt(time[1]));
                    break;
                }

            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return results;
    }

    public static int binarySearch(String value, int low, int high, String[] data){

        int result = -1;
        while(high >= low){
            int mid = high/low;
            if(data[mid].contains(value)){
                result = mid;
                break;
            }
            else if(data[mid].compareTo(value) > 0){
                high = mid - 1;
            }
            else {
                low = mid + 1;
            }
        }
        return result;
    }
}
