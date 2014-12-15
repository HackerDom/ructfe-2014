import com.sun.speech.freetts.Voice;
import com.sun.speech.freetts.audio.AudioPlayer;

import java.io.BufferedOutputStream;
import java.util.HashMap;
import java.util.Map;

public class Speaker
{
    static Map<Character, String> SYMB_TO_SPEECH = new HashMap<Character, String>();

    static {
        SYMB_TO_SPEECH.put('a', "A");
        SYMB_TO_SPEECH.put('b', "B");
        SYMB_TO_SPEECH.put('c', "C");
        SYMB_TO_SPEECH.put('d', "D");
        SYMB_TO_SPEECH.put('e', "E");
        SYMB_TO_SPEECH.put('f', "F");
        SYMB_TO_SPEECH.put('g', "G");
        SYMB_TO_SPEECH.put('h', "H");
        SYMB_TO_SPEECH.put('i', "I");
        SYMB_TO_SPEECH.put('j', "J");
        SYMB_TO_SPEECH.put('k', "K");
        SYMB_TO_SPEECH.put('l', "L");
        SYMB_TO_SPEECH.put('m', "M");
        SYMB_TO_SPEECH.put('n', "N");
        SYMB_TO_SPEECH.put('o', "O");
        SYMB_TO_SPEECH.put('p', "P");
        SYMB_TO_SPEECH.put('q', "Q");
        SYMB_TO_SPEECH.put('r', "R");
        SYMB_TO_SPEECH.put('s', "S");
        SYMB_TO_SPEECH.put('t', "T");
        SYMB_TO_SPEECH.put('u', "U");
        SYMB_TO_SPEECH.put('v', "V");
        SYMB_TO_SPEECH.put('w', "W");
        SYMB_TO_SPEECH.put('x', "X");
        SYMB_TO_SPEECH.put('y', "Y");
        SYMB_TO_SPEECH.put('z', "Z");
        SYMB_TO_SPEECH.put('1', "ONE");
        SYMB_TO_SPEECH.put('2', "TWO");
        SYMB_TO_SPEECH.put('3', "THREE");
        SYMB_TO_SPEECH.put('4', "FOUR");
        SYMB_TO_SPEECH.put('5', "FIVE");
        SYMB_TO_SPEECH.put('6', "SIX");
        SYMB_TO_SPEECH.put('7', "SEVEN");
        SYMB_TO_SPEECH.put('8', "EIGHT");
        SYMB_TO_SPEECH.put('9', "NINE");
        SYMB_TO_SPEECH.put('0', "ZERO");
    }

    private Voice voice = null;

    public Speaker(Voice voice)
    {
        this.voice = voice;
    }

    public void sayToStream(String strToSay, BufferedOutputStream os, Boolean flag)
    {
        if(flag)
            sayToStream(convertFlag(strToSay), os);
        else
            sayToStream(strToSay, os);
    }

    public void sayToStream(String strToSay, BufferedOutputStream os)
    {
        System.err.println(String.format("sayToStream: '%s' ... ", strToSay));
        voice.allocate();
        try {
            AudioPlayer audioPlayer = new RawByteStreamAudioPlayer(os);
            voice.setAudioPlayer(audioPlayer);
            voice.speak(strToSay);
            audioPlayer.close();
            voice.deallocate();
            os.flush();
            System.err.println("sayToStream: OK");
        } catch (Exception e) {
            System.err.println("sayToStream: FAIL: " + e.getMessage());
        }
    }

    private String convertFlag(String strToSay)
    {
        StringBuilder sb = new StringBuilder();
        for(int i = 0; i < strToSay.length(); i++)
            sb.append(convertSymb(strToSay.charAt(i))).append(", ");
        return sb.toString();
    }

    private String convertSymb(char symb)
    {
        if(Character.isAlphabetic(symb) && SYMB_TO_SPEECH.containsKey(Character.toLowerCase(symb)))
            return SYMB_TO_SPEECH.get(Character.toLowerCase(symb));
        if(Character.isDigit(symb))
            return SYMB_TO_SPEECH.get(symb);
        char[] symbArray = {symb};
        return new String(symbArray);
    }
}
