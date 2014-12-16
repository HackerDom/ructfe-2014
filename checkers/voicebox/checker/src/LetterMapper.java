import java.util.Hashtable;

public class LetterMapper
{
    private String [] words =
    {
        "apple",
        "bubble",
        "calculate",
        "daemon",
        "earth",
        "flamingo",
        "golem",
        "help",
        "icon",
        "jaguar",
        "kilogram",
        "large",
        "mother",
        "nuts",
        "option",
        "pig",
        "quin",
        "rang",
        "stop",
        "tank",
        "uncle",
        "village",
        "window",
        "x-ray",
        "yahoo",
        "zipper"
    };

    private Hashtable<Character, String> hash = new Hashtable<Character, String>();

    public LetterMapper()
    {
        for (String w : words)
            hash.put(w.charAt(0), w);
        for (Integer i=0; i<10; i++)
            hash.put(Character.forDigit(i, 10), i.toString());
        hash.put('=', "equals");
    }

    private String mapChar(char c) throws Exception
    {
        if (!hash.containsKey(c))
            throw new Exception("Char " + c + " was not found");
        return hash.get(c);
    }

    public String mapString(String s) throws Exception
    {
        s = s.toLowerCase();
        StringBuilder sb = new StringBuilder();

        for (int i=0; i<s.length(); i++) {
            sb.append(mapChar(s.charAt(i)) + " ");
        }

        return sb.toString().trim();
    }
}
