import com.sun.speech.freetts.Voice;
import com.sun.speech.freetts.VoiceManager;

import java.io.*;
import java.net.Socket;
import java.util.Arrays;

public class Checker {

    private static final int CODE_OK = 101;
    private static final int CODE_CORRUPT = 102;
    private static final int CODE_MUMBLE = 103;
    private static final int CODE_DOWN = 104;
    private static final int CODE_CHECKER_ERROR = 110;

    private static Integer PORT = 1337;

    private static String CMD;

    public static void main(String[] args)
    {
        try {
            if (args.length < 2 || args.length > 4)
                throw new CheckerError("Wrong arguments count");

            CMD = args[0];
            args = Arrays.copyOfRange(args, 1, args.length);

            if (CMD.equals("check"))
                check(args);
            else if (CMD.equals("put"))
                put(args);
            else if (CMD.equals("get"))
                get(args);
            else if (CMD.equals("list"))    // TODO: kill
                list(args);
            else if (CMD.equals("test"))    // TODO: kill
                test(args);
            else
                exitCheckerError("Unknown command: " + CMD);

            exitCheckerError("Command '" + CMD + "' didn't specify exit code");
        }
        catch (Exception e) {
            e.printStackTrace();
            exitCheckerError(e.getMessage());
        }
    }

    private static void test(String[] args)
    {
        Client client = new Client(args[0], PORT);

        String response;

/*        client.say("ok box");
        client.say("authorization");
        client.say("hello");*/

        client.say("ok box");
        client.say("registration");
        client.say("hello");

        client.close();
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
        exitCheckerError("Not implemented");
    }

    private static void put(String[] args) throws CheckerError
    {
        if (args.length != 3)
            exitCheckerError("Usage: Checker put <host> <id> <flag>");
        exitCheckerError("Not implemented");
    }

    private static void check(String[] args) throws CheckerError
    {
        if (args.length != 1)
            exitCheckerError("Usage: Checker check <host>");

        String HOST = args[0];
        Client client = new Client(HOST, PORT);

        String response;

        response = client.say("ok box");
        if (!response.startsWith("authorization or registration"))
            exitMumble("Unexpected response at check (step 1)");

        response = client.say("registration");
        if (!response.startsWith("say: "))
            exitMumble("Unexpected response at check (step 2)");

        exitOK("Service seems to be OK");
        client.close();
    }

    private static void sayFlagToStream(Speaker speaker, String flagToSay, BufferedOutputStream stream)
    {
        speaker.sayToStream(flagToSay, stream, true);
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
