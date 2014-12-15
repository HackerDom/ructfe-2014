import com.sun.speech.freetts.Voice;
import com.sun.speech.freetts.VoiceManager;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetSocketAddress;
import java.net.Socket;

public class Client
{
    private static final int CONNECT_TIMEOUT = 5000;
    private static final int READ_TIMEOUT = 5000;

    private static final String VOICE_NAME = "mbrola_us2";
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

        System.err.printf("Connected to %s:%d\n", host, port);
    }

    public String say(String data)
    {
        Speaker speaker = getSpeaker(); // Один спикер на все запросы не работает
        speaker.sayToStream(data, out);
        try {
            String response = in.readLine();
            System.err.println(String.format("Response: '%s'", response));
            return response;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
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

    private static Speaker getSpeaker()
    {
        VoiceManager voiceManager = VoiceManager.getInstance();
        Voice voice = voiceManager.getVoice(VOICE_NAME);

        if (voice == null)
            Checker.exitCheckerError("Cannot find voice '" + VOICE_NAME + "'");

        return new Speaker(voice);
    }
}
