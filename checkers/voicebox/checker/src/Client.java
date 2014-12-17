import com.sun.speech.freetts.Voice;
import com.sun.speech.freetts.VoiceManager;

import java.io.*;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.Date;

public class Client
{
    private static final int CONNECT_TIMEOUT = 12000;
    private static final int READ_TIMEOUT = 12000;
    private static final Boolean SAVE_FILES = false;

    private static final String VOICE_NAME = "mbrola_us3";
    private static final String SERVER_CHARSET = "UTF-16";

    private Socket s = null;
    private BufferedOutputStream out = null;
    private BufferedReader in = null;

    public Client(String host, int port)
    {
        try {
            s = new Socket();
            s.connect(new InetSocketAddress(host, port), CONNECT_TIMEOUT);
            s.setSoTimeout(READ_TIMEOUT);
            out = new BufferedOutputStream(s.getOutputStream());
            in = new BufferedReader(new InputStreamReader(s.getInputStream(), SERVER_CHARSET));
        }
        catch (IOException e) {
            Checker.exitDown(e.getMessage());
        }

        Checker.log("Connected to %s:%d", host, port);
    }

    private static void write(String data, BufferedOutputStream outStream)
    {
        Speaker speaker = newSpeaker();         // Один спикер на все запросы не работает
        speaker.sayToStream(data, outStream);
    }

    private String read()
    {
        try {
            long start = System.nanoTime();
            String response = in.readLine();
            long duration = System.nanoTime() - start;
            System.err.println(String.format("<- '%s' (%d ms)", response, duration/1000000));
            return response;
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }
    }

    public String say(String data)
    {
        data = data.trim();
        if (SAVE_FILES) {
            try {
                Date date = new Date();
                String fileName = "say_" + date.getTime() + ".pcm";
                FileOutputStream outFile = new FileOutputStream(fileName);
                Checker.log("xx '%s' (write to file: '%s')", data, fileName);
                write(data, new BufferedOutputStream(outFile));
                outFile.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        Checker.log("-> '%s'", data);
        write(data, out);
        return read();
    }

    public void close()
    {
        try {
            if (out != null) out.close();
        }
        catch (Exception e) { }

        try {
            if (in != null) in.close();
        }
        catch (Exception e) { }

        try {
            if (s != null) s.close();
        }
        catch (Exception e) { }
    }

    private static Speaker newSpeaker()
    {
        VoiceManager voiceManager = VoiceManager.getInstance();
        Voice voice = voiceManager.getVoice(VOICE_NAME);

        if (voice == null)
            Checker.exitCheckerError("Cannot find voice '" + VOICE_NAME + "'");

        return new Speaker(voice);
    }
}
