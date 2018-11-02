import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class SearchDriver {

    public static void main(String[] args) {

        long start = System.nanoTime();
        System.out.println("Total number of users from Nebraska fan200 = " + numPeopleFromNebraska(200));
        long end = System.nanoTime();
        System.out.println("Search for num people from Nebraska using fan200: " + (end - start)/1000000000.0 + "seconds.");
        start = System.nanoTime();
        System.out.println("Total number of users from Nebraska fan10 = " + numPeopleFromNebraska(10));
        end = System.nanoTime();
        System.out.println("Search for num people from Nebraska using fan10: " + (end - start)/1000000000.0 + "seconds.");
        start = System.nanoTime();
        System.out.println("Total number of users who sent messages between 8-9am fan200 = " + numPeopleWithMessageBetween("08:00:00", "09:00:00",200));
        end = System.nanoTime();
        System.out.println("Search number of users who sent messages between 8-9am fan200: " + (end - start)/1000000000.0 + "seconds.");
        start = System.nanoTime();
        System.out.println("Total number of users who sent messages between 8-9am fan10 = " + numPeopleWithMessageBetween("08:00:00", "09:00:00",10));
        end = System.nanoTime();
        System.out.println("Search number of users who sent messages between 8-9am fan10: " + (end - start)/1000000000.0 + "seconds.");
        start = System.nanoTime();
        System.out.println("Total number of users from Nebraska who sent messages between 8-9am fan10 = " + numPeopleFromNebraskaWithMessagesBetween("08:00:00", "09:00:00",10));
        end = System.nanoTime();
        System.out.println("Search number of users from Nebraska who sent messages between 8-9am fan10: " + (end - start)/1000000000.0 + "seconds.");
        start = System.nanoTime();
        System.out.println("Total number of users from Nebraska who sent messages between 8-9am fan200 = " + numPeopleFromNebraskaWithMessagesBetween("08:00:00", "09:00:00",200));
        end = System.nanoTime();
        System.out.println("Search number of users from Nebraska who sent messages between 8-9am fan200: " + (end - start)/1000000000.0 + "seconds.");
        start = System.nanoTime();
        System.out.println("User from Nebraska who sent the most messages between 8-9am fan10 = " + personFromNebraskaWithGreatestNumMessagesBetween("08:00:00", "09:00:00",10));
        end = System.nanoTime();
        System.out.println("Search user from Nebraska who sent the most messages between 8-9am fan10: " + (end - start)/1000000000.0 + "seconds.");
        start = System.nanoTime();
        System.out.println("User from Nebraska who sent the most messages between 8-9am fan200 =  " + personFromNebraskaWithGreatestNumMessagesBetween("08:00:00", "09:00:00",200));
        end = System.nanoTime();
        System.out.println("Search user from Nebraska who sent the most messages between 8-9am fan200: " + (end - start)/1000000000.0 + "seconds.");


    }

    public static int numPeopleFromNebraskaWithMessagesBetween(String start, String end, int fan){
        String stateId = Integer.toString(findStateID("Nebraska", fan));
        List<Integer> timeIds = findTimeIDs(start, end, fan);
        Set<Integer> statePersonIds = getPersonIdsFromStateId(fan,stateId);
        Set<Integer> personIds = new HashSet<>();
        for(int i : timeIds){
            personIds.addAll(getPersonIdsFromTime(fan, i));
        }
        statePersonIds.retainAll(personIds);
        return statePersonIds.size();
    }

    public static int personFromNebraskaWithGreatestNumMessagesBetween(String start, String end, int fan){
        String stateId = Integer.toString(findStateID("Nebraska", fan));
        List<Integer> timeIds = findTimeIDs(start, end, fan);
        Set<Integer> statePersonIds = getPersonIdsFromStateId(fan,stateId);
        List<Integer> personIds = new ArrayList<>();
        for(int i : timeIds){
            personIds.addAll(getPersonIdsFromTime(fan, i));
        }
        Map<Integer, Integer> myMap = new HashMap<>();
        for(int personId: personIds){
            if(statePersonIds.contains(personId)){
                if(myMap.containsKey(personId)){
                    myMap.put(personId, myMap.get(personId) + 1);
                }
                else {
                    myMap.put(personId, 1);
                }
            }
        }
        int currPersonId = -1;
        int currMax = Integer.MIN_VALUE;
        for (int key : myMap.keySet()) {
            if(myMap.get(key) >= currMax){
                currPersonId = key;
                currMax = myMap.get(key);
            }
        }
        return currPersonId;
    }

    public static int numPeopleFromNebraska(int fan){
        String stateId = Integer.toString(findStateID("Nebraska", fan));
        return getPersonIdsFromStateId(fan,stateId).size();
    }

    public static int numPeopleWithMessageBetween(String start, String end, int fan){

        List<Integer> result = findTimeIDs(start, end, fan);
        Set<Integer> personIds = new HashSet<>();
        for(int i : result){
            personIds.addAll(getPersonIdsFromTime(fan, i));
        }
        return personIds.size();
    }

    public static Set<Integer> getPersonIdsFromStateId(int fan, String stateId){
        String nextFile = searchNodeFile("data/persons/fan" + fan + "/person_node_0", stateId);
        while(nextFile.contains("person_node")){
            nextFile = searchNodeFile("data/persons/fan" + fan + "/" + nextFile, stateId);
        }
        List<Integer> result = searchLeafFileRange("data/persons/fan" + fan + "/" + nextFile, stateId, stateId);
        Set<Integer> results = new HashSet<>(result);
        return results;
    }

    public static List<Integer> getPersonIdsFromTime(int fan, int id){
        String idString = Integer.toString(id);
        String nextFile = searchNodeFile("data/messages/fan" + fan + "/messages_node_0", idString);
        while(nextFile.contains("messages_node")){
            nextFile = searchNodeFile("data/messages/fan" + fan + "/" + nextFile, idString);
        }
        List<Integer> result = searchLeafFileRange("data/messages/fan" + fan + "/" + nextFile, idString, idString);
        return result;
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
                if(i%2 != 0) {
                    int compare;
                    if(file.contains("messages")){
                        compare = Integer.parseInt(searchValue) - Integer.parseInt(data[i].split(";")[0]);
                    }
                    else {
                        compare = searchValue.compareTo(data[i]);
                    }
                    if(compare <= 0){
                        if(compare < 0){
                            result = data[i - 1];
                        }
                        else {
                            result = data[i + 1];
                        }
                        break;
                    }
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
            int currIndex;
            if(file.contains("messages")){
                currIndex = binarySearchId(Integer.parseInt(start), 1, data.length - 2, data);
            }
            else {
                currIndex = binarySearch(start, 1, data.length - 2, data);
            }
            int prevIndex = -1;
            while(currIndex == 1){
                String[] filePieces = file.split("/");
                String[] filePointer = filePieces[3].split("_");
                int pointer = Integer.parseInt(filePointer[2]);
                if(pointer > 0){
                   file = filePieces[0] + "/" + filePieces[1] + "/" + filePieces[2] + "/"
                            + filePointer[0] + "_" + filePointer[1] + "_" + (pointer - 1);
                    br = new BufferedReader(new FileReader(file));
                    String[] newData = br.readLine().split(",");
                    if(file.contains("messages")){
                        prevIndex = currIndex;
                        currIndex = binarySearchId(Integer.parseInt(start), 1, data.length - 2, data);
                    }
                    else {
                        prevIndex = currIndex;
                        currIndex = binarySearch(start, 1, data.length - 2, data);
                    }
                    if(currIndex < 0){
                        currIndex = prevIndex;
                        break;
                    }
                    if(currIndex == 1){
                        data = newData;
                    }
                }
            }


            if(file.contains("messages")){
                int currData = Integer.parseInt(data[currIndex].split(";")[0]);
                int newEnd = Integer.parseInt(end);
                while(currData - newEnd <= 0){
                    String[] entryVals = data[currIndex].split(";");
                    if(entryVals.length > 1){
                        results.add(Integer.parseInt(entryVals[3]));
                    }
                    currIndex++;
                    if(currIndex == data.length-1){
                        String[] fileName = file.split("/");
                        file = fileName[0] + "/" + fileName[1] + "/" + fileName[2] + "/" + data[currIndex];
                        br = new BufferedReader(new FileReader(file));
                        data = br.readLine().split(",");
                        currIndex = 1;
                    }
                    currData = Integer.parseInt(data[currIndex].split(";")[0]);
                }
            }
            else {
                while(data[currIndex].compareTo(end) <= 0 || data[currIndex].contains(end)){
                    String[] entryVals = data[currIndex].split(";");
                    if(file.contains("time")){
                        results.add(Integer.parseInt(entryVals[1]));
                    }
                    else if(file.contains("person")){
                        results.add(Integer.parseInt(entryVals[1]));
                    }
                    currIndex++;
                    if(currIndex == data.length-1){
                        String[] fileName = file.split("/");
                        file = fileName[0] + "/" + fileName[1] + "/" + fileName[2] + "/" + data[currIndex];
                        br = new BufferedReader(new FileReader(file));
                        data = br.readLine().split(",");
                        currIndex = 1;
                    }
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
            if(data[mid].split(";")[0].contains(value)){
                int currIndex = mid;
                if(data[mid -1].split(";")[0].contains(value)){
                    while(data[currIndex].split(";")[0].contains(value)){
                        currIndex = currIndex-1;
                    }
                    currIndex = currIndex + 1;
                }
                result = currIndex;
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

    public static int binarySearchId(int value, int low, int high, String[] data){

        int result = -1;
        while(high >= low){
            int mid = high/low;
            int compVal = Integer.parseInt(data[mid].split(";")[0]);
            if(value - compVal == 0){
                int currIndex = mid;
                if(mid - 1 != 0){
                    compVal = Integer.parseInt(data[mid - 1].split(";")[0]);
                }
                else {
                    return 1;
                }
                if(value - compVal == 0){
                    compVal = Integer.parseInt(data[currIndex].split(";")[0]);
                    while(value - compVal == 0){
                        currIndex = currIndex-1;
                        if(currIndex == 0){
                            return 1;
                        }
                        else {
                            compVal = Integer.parseInt(data[currIndex].split(";")[0]);
                        }
                    }
                    currIndex = currIndex + 1;
                }
                result = currIndex;
                break;
            }
            else if(compVal - value > 0){
                high = mid - 1;
            }
            else {
                low = mid + 1;
            }
        }
        return result;
    }
}
