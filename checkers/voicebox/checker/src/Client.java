import com.sun.speech.freetts.Voice;
import com.sun.speech.freetts.VoiceManager;
import com.sun.speech.freetts.audio.AudioPlayer;

import java.io.*;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.Date;
import java.util.zip.Deflater;
import java.util.zip.GZIPOutputStream;

public class Client
{
    private static final int CONNECT_TIMEOUT = 12000;
    private static final int READ_TIMEOUT = 12000;

    private static final Boolean SAVE_PCM = false;
    private static final Boolean SAVE_GZIP = false;
    private String SAVE_PREFIX = "";

    private static final String VOICE_NAME = "mbrola_us3";
    private static final String SERVER_CHARSET = "UTF-16";

    private Socket s = null;
    private OutputStream out = null;
    private BufferedReader in = null;

    public Client(String host, int port)
    {
        SAVE_PREFIX = host;
        try {
            s = new Socket();
            s.connect(new InetSocketAddress(host, port), CONNECT_TIMEOUT);
            s.setSoTimeout(READ_TIMEOUT);
            out = s.getOutputStream();
            in = new BufferedReader(new InputStreamReader(s.getInputStream(), SERVER_CHARSET));
        }
        catch (IOException e) {
            Checker.exitDown(e.getMessage());
        }

        Checker.log("Connected to %s:%d", host, port);
    }

    private static void write(String data, OutputStream outStream, boolean useGzip)
    {
        try {
            OutputStream stream = useGzip ? new GZIPOutputStream(outStream){{def.setLevel(Deflater.BEST_COMPRESSION);}} : outStream;
            sayToStream(data, stream);
            if (useGzip)
                ((GZIPOutputStream) stream).finish();
            stream.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String read()
    {
        try {
            long start = System.nanoTime();
            String response = in.readLine();
            long duration = System.nanoTime() - start;
            Checker.log("<- '%s' (%d ms)", response == null ? "<NULL>" : response, duration / 1000000);
            return response;
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }
    }

    private String getFileName(String extension)
    {
        return String.format("say_%s_%d.%s", SAVE_PREFIX, System.nanoTime(), extension);
    }

    public void writeDebugFile(String data, String extension, boolean useGzip) {
        try {
            String fileName = getFileName(extension);

            FileOutputStream outFile = new FileOutputStream(fileName);
            write(data, outFile, useGzip);
            outFile.close();

            File file = new File(fileName);
            Checker.log("xx '%s' (write to file: '%s', %d bytes)", data, fileName, file.length());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public String say(String data)
    {
        data = data.trim();
        if (SAVE_PCM)
            writeDebugFile(data, "pcm", false);
        if (SAVE_GZIP)
            writeDebugFile(data, "gzip", true);

        Checker.log("-> '%s'", data);
        write(data, out, true);
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

    private static void sayToStream(String data, OutputStream stream)
    {
        VoiceManager voiceManager = VoiceManager.getInstance();
        Voice voice = voiceManager.getVoice(VOICE_NAME);

        if (voice == null)
            Checker.exitCheckerError("Cannot find voice '" + VOICE_NAME + "'");

        voice.allocate();
        try {
            AudioPlayer player = new RawByteStreamAudioPlayer(stream);
            voice.setAudioPlayer(player);
            voice.speak(data);
            player.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        finally {
            voice.deallocate();
        }
    }
}
