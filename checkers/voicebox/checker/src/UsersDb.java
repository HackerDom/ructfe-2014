import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class UsersDb
{
    private final static String dirName = "users.db";
    private final static Charset CHARSET = StandardCharsets.UTF_8;

    public UsersDb()
    {
        new File(dirName).mkdir();
    }

    private Path createPath(String key)
    {
        return Paths.get(dirName, key);
    }

    public void put(String key, String value)
    {
        List<String> lines = new ArrayList<String>();
        lines.add(value);
        try {
            Files.write(createPath(key), lines, CHARSET);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String get(String key)
    {
        try {
            List<String> lines = Files.readAllLines(createPath(key), CHARSET);
            return lines.isEmpty() ? "" : lines.get(0);
        } catch (IOException e) {
            return "1";
        }
    }
}
