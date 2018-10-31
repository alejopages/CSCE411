import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class SearchDriver {

    public static void main(String[] args) {
        System.out.println(findStateID());
    }

    public static int findStateID(){

        String nextFile = searchNodeFile("data/states/fan10/state_node_0", "Nebraska");
        System.out.println(nextFile);
        while(nextFile.contains("state_node")){
            nextFile = searchNodeFile("data/states/fan10/" + nextFile, "Nebraska");
        }
        int result = searchLeafFile("data/states/fan10/" + nextFile, "Nebraska");
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
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return result;
    }

    public static int searchLeafFile(String file, String searchValue){
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
