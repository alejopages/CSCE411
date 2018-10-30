import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConnection {
    private static String username = "cfarmer";
    private static String password = "eKd65T";
    private static String url = "jdbc:mysql://cse.unl.edu/cfarmer?useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC";
    private static String driverString = "com.mysql.cj.jdbc.Driver";
    private static Connection conn = null;

    public static Connection getConnection(){

        try {
            Class.forName(driverString);
            conn = DriverManager.getConnection(url, username, password);
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return conn;
    }
}
