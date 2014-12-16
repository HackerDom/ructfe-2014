import com.sun.speech.freetts.Voice;
import com.sun.speech.freetts.audio.AudioPlayer;

import java.io.BufferedOutputStream;
import java.util.HashMap;
import java.util.Map;

public class Speaker
{
    static Map<Character, String> SYMB_TO_SPEECH = new HashMap<Character, String>();

    private Voice voice = null;

    public Speaker(Voice voice)
    {
        this.voice = voice;
    }

    public void sayToStream(String strToSay, BufferedOutputStream os)
    {
//        voice.setPitch((float)(57));
//        voice.setPitchShift((float)(2.5));
//        voice.setPitchRange((float)(5)); //mutace
//        voice.setStyle("casual");  //"business", "casual", "robotic", "breathy"
//        voice.setDurationStretch(1.5f);
        voice.allocate();
        try {
            AudioPlayer audioPlayer = new RawByteStreamAudioPlayer(os);
            voice.setAudioPlayer(audioPlayer);
            voice.speak(strToSay);
            audioPlayer.close();
            voice.deallocate();
            os.flush();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
