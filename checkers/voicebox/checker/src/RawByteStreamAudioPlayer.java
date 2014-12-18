import com.sun.speech.freetts.audio.AudioPlayer;

import javax.sound.sampled.AudioFormat;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.ByteBuffer;

public class RawByteStreamAudioPlayer implements AudioPlayer
{
    private static final Boolean DEBUG = false;

    private AudioFormat audioFormat;
    private float volume;
    private OutputStream os;
    private int iteration = 0;
    private int totalBytes = 0;

    public RawByteStreamAudioPlayer(OutputStream os)
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
            totalBytes += 4;
            if (DEBUG) {
                Checker.log("  [RawByteStreamAudioPlayer] Written end (4 bytes), value = 0");
                Checker.log("  [RawByteStreamAudioPlayer] Total (uncompressed) bytes sent: %d", totalBytes);
            }
        } catch (IOException e) {
            e.printStackTrace();
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
            if (DEBUG)
                Checker.log("  [RawByteStreamAudioPlayer] Written size (4 bytes), value = %d", size);

            os.write(bytes, offset, size);
            if (DEBUG)
                Checker.log("  [RawByteStreamAudioPlayer] Written data (%d bytes), iteration = %d", size, iteration++);

            totalBytes += 4 + size;
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }

    @Override
    public void showMetrics() {

    }
}
