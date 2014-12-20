import java.io.File;
import java.io.FileNotFoundException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.*;
import java.util.List;

public class SqlUsersDb implements IUsersDb
{
    /* alter user voicebox password '1234qwer';
     * create database voicebox owner voicebox;
     * \c voicebox
     * create table users(key varchar(16) primary key, value varchar(8));
     */

    private static final Charset CONF_CHARSET = StandardCharsets.UTF_8;
    private static final String CONF_NAME = "SqlUsersDb.conf";

    private static final String DEFAULT_ID = "1";

    private final String url;
    private final String name;
    private final String password;

    public SqlUsersDb() throws Exception
    {
        Class.forName("org.postgresql.Driver");

        if (!configExists())
            throw new FileNotFoundException("Config file not found: " + CONF_NAME);

        List<String> lines = Files.readAllLines(Paths.get(CONF_NAME), CONF_CHARSET);
        if (lines.size() != 3)
            throw new Exception("Invalid lines count (must be 3: url, user, password)");

        url = lines.get(0);
        name = lines.get(1);
        password = lines.get(2);
    }

    public static Boolean configExists()
    {
        return new File(CONF_NAME).exists();
    }

    private Connection connect() throws SQLException
    {
        return DriverManager.getConnection(url, name, password);
    }

    private void safeClose(Statement statement)
    {
        try {
            if (statement != null) statement.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void safeClose(Connection connection)
    {
        try {
            if (connection != null) connection.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void put(String key, String value)
    {
        Connection conn = null;
        PreparedStatement stDelete = null;
        PreparedStatement stInsert = null;
        try {
            conn = connect();

            stDelete = conn.prepareStatement("DELETE FROM users WHERE key = ?");
            stDelete.setString(1, key);
            stDelete.execute();

            stInsert = conn.prepareStatement("INSERT INTO users (key,value) VALUES (?, ?)");
            stInsert.setString(1, key);
            stInsert.setString(2, value);
            stInsert.execute();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            safeClose(stDelete);
            safeClose(stInsert);
            safeClose(conn);
        }
    }

    public String get(String key)
    {
        Connection conn = null;
        PreparedStatement stSelect = null;
        try {
            conn = connect();
            stSelect = conn.prepareStatement("SELECT value FROM users WHERE key = ?");
            stSelect.setString(1, key);
            ResultSet rs = stSelect.executeQuery();
            while (rs.next()) {
                return rs.getString(1);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            safeClose(stSelect);
            safeClose(conn);
        }

        return DEFAULT_ID;
    }
}
