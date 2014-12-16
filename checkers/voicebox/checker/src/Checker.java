import com.sun.speech.freetts.Voice;
import com.sun.speech.freetts.VoiceManager;

import java.util.Arrays;
import java.util.Random;

public class Checker {

    private static final int CODE_OK            = 101;
    private static final int CODE_CORRUPT       = 102;
    private static final int CODE_MUMBLE        = 103;
    private static final int CODE_DOWN          = 104;
    private static final int CODE_CHECKER_ERROR = 110;

    private static Integer PORT = 1337;
    private static final int FLAGID_LEN = 16;

    private static Random random = new Random();
    private static LetterMapper letterMapper = new LetterMapper();

    public static void main(String[] args)
    {
        try {
            if (args.length == 0)
                exitCheckerError("Give command as first argument (check/put/get)");

            String CMD = args[0];
            args = Arrays.copyOfRange(args, 1, args.length);

            if (CMD.equals("check"))      check(args);
            else if (CMD.equals("put"))   put(args);
            else if (CMD.equals("get"))   get(args);
            else if (CMD.equals("list"))  list(args);
            else exitCheckerError("Unknown command: " + CMD);

            exitCheckerError("Command '" + CMD + "' didn't specify exit code");
        }
        catch (Exception e) {
            e.printStackTrace();
            exitCheckerError(e.getMessage());
        }
    }

    private static void list(String[] args)
    {
        System.out.println("All voices available:");
        VoiceManager voiceManager = VoiceManager.getInstance();
        for (Voice v : voiceManager.getVoices())
            System.out.println("    " + v.getName() + " (" + v.getDomain() + " domain)");
        exitOK("OK");
    }

    private static void get(String[] args) throws CheckerError
    {
        if (args.length != 3)
            exitCheckerError("Usage: Checker get <host> <id> <flag>");

        String HOST = args[0];
        String ID = args[1];
        String FLAG = args[2];

        String mappedFlag = null;
        try {
            mappedFlag = letterMapper.mapString(FLAG);
        } catch (Exception e) {
            e.printStackTrace();
            exitCheckerError("Cannot map flag");
        }

        String response;

        Client client = new Client(HOST, PORT);

        testForMumble(client.say("ok box"), "authorization or registration");

        testForMumble(response = client.say("authorization"), "say:");

        testForMumble(client.say(response.replaceFirst("say:", "")), "welcome again");

        response = client.say(String.format("get %s", splitWithSpaces(ID)));
        if (response.equals(mappedFlag))
            exitOK("Flag found");
        else
            exitCorrupt("Flag not found (looked for '" + mappedFlag + "')");
    }

    private static void put(String[] args) throws CheckerError
    {
        if (args.length != 3)
            exitCheckerError("Usage: Checker put <host> <id> <flag>");

        String HOST = args[0];
        String FLAG = args[2];

        String ID = newFlagId();
        log("newFlagId: %s", ID);

        String response;

        Client client = new Client(HOST, PORT);

        testForMumble(client.say("ok box"), "authorization or registration");
        testForMumble(response = client.say("authorization"), "say:");
        response = client.say(response.replaceFirst("say:", ""));

        if (response.startsWith("unknown user"))
        {
            client.close();

            log("No problem. I will try to register new user");

            client = new Client(HOST, PORT);

            testForMumble(client.say("ok box"), "authorization or registration");
            testForMumble(response = client.say("registration"), "say: ");
            testForMumble(client.say(response.replaceFirst("say:", "")), "your name");
            testForMumble(client.say("user"), "welcome");

            client.close();

            // Authorize

            log("Registered new user OK. Trying to login");

            client = new Client(HOST, PORT);

            testForMumble(client.say("ok box"), "authorization or registration");
            testForMumble(response = client.say("authorization"), "say:");
            response = client.say(response.replaceFirst("say:", ""));
        }
        testForMumble(response, "welcome again");

        String mappedFlag = null;
        try {
            mappedFlag = letterMapper.mapString(FLAG);
        } catch (Exception e) {
            e.printStackTrace();
            exitCheckerError("Failed to create mappedFlag");
        }
        response = client.say(String.format("put id %s idea %s", splitWithSpaces(ID), mappedFlag));
        testForMumble(response, "Idea put with id: " + ID);
        if (!response.contains(mappedFlag))
            exitCorrupt("Cannot find flag in response");

        System.out.println(ID.replaceAll(" ", ""));         // Новый ID флага для Checksystem
        exitOK("Success");
    }

    private static void check(String[] args) throws CheckerError
    {
        if (args.length != 1)
            exitCheckerError("Usage: Checker check <host>");

        String HOST = args[0];
        Client client = new Client(HOST, PORT);

        testForMumble(client.say("ok box"), "authorization or registration");

        exitOK("Service seems to be OK");
        client.close();
    }

    private static String newFlagId()
    {
        StringBuilder sb = new StringBuilder();
        Integer prevDigit = -1;
        for (int i=0; i<FLAGID_LEN; i++)
        {
            Integer digit;
            do {
                digit = random.nextInt(10);
            } while (digit == prevDigit);
            sb.append(digit.toString());
            prevDigit = digit;
        }
        return sb.toString();
    }

    private static String splitWithSpaces(String data)
    {
        return Arrays.toString(data.split("")).replaceAll(", ", " ").replaceAll("[\\[\\]]", "").trim();
    }

    private static void testForMumble(String response, String startsWith)
    {
        if (!response.toLowerCase().startsWith(startsWith.toLowerCase()))
            exitMumble("Service response: '" + response + "'. Expected: '" + startsWith + "'");
    }

    public static void log(String message)
    {
        System.err.println(message);
    }

    public static void log(String format, Object ... args)
    {
        log(String.format(format, args));
    }

    private static void exit(String message, int code)
    {
        System.err.println(code + ": " + message);
        System.exit(code);
    }

    public static void exitOK(String message)
    {
        exit(message, CODE_OK);
    }

    public static void exitMumble(String message)
    {
        exit(message, CODE_MUMBLE);
    }

    public static void exitCorrupt(String message)
    {
        exit(message, CODE_CORRUPT);
    }

    public static void exitDown(String message)
    {
        exit(message, CODE_DOWN);
    }

    public static void exitCheckerError(String message)
    {
        exit(message, CODE_CHECKER_ERROR);
    }
}
