import com.sun.speech.freetts.audio.AudioPlayer;

import javax.sound.sampled.AudioFormat;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

public class RawByteStreamAudioPlayer implements AudioPlayer
{
    private AudioFormat audioFormat;
    private float volume;
    private BufferedOutputStream os;

    public RawByteStreamAudioPlayer(BufferedOutputStream os)
    {
        this.os = os;
    }

    @Override
    public void setAudioFormat(AudioFormat audioFormat) {
        this.audioFormat = audioFormat;
    }

    @Override
    public AudioFormat getAudioFormat() {
        return audioFormat;
    }

    @Override
    public void pause() {}

    @Override
    public void resume() {}

    @Override
    public void reset() {}

    @Override
    public boolean drain() {
        return true;
    }

    @Override
    public void begin(int i) {}

    @Override
    public boolean end() {
        return true;
    }

    @Override
    public void cancel() {

    }

    @Override
    public void close() {
        try {
            byte[] bts = ByteBuffer.allocate(4).putInt(0).array();
            os.write(bts, 0, 4);
            os.flush();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }

    @Override
    public float getVolume() {
        return volume;
    }

    @Override
    public void setVolume(float volume) {
        this.volume = volume;
    }

    @Override
    public long getTime() {
        return -1L;
    }

    @Override
    public void resetTime() {

    }

    @Override
    public void startFirstSampleTimer() {

    }

    @Override
    public boolean write(byte[] audioData) {
        return write(audioData, 0, audioData.length);
    }

    @Override
    public boolean write(byte[] bytes, int offset, int size) {
        try {
            byte[] bts = ByteBuffer.allocate(4).putInt(size).array();
            os.write(bts, 0, 4);
            os.write(bytes, offset, size);
        } catch (IOException ioe) {
            return false;
        }
        return true;
    }

    @Override
    public void showMetrics() {

    }
}
