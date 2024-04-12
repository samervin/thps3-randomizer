import java.io.File;
import java.nio.ByteBuffer;
import java.util.HashMap;
import java.util.Map;

public class QbFileHandler {
  private Map<Integer, String> fields;
  
  private ImprovedByteStream byteStream;
  
  public Map<Integer, String> getFields() {
    return this.fields;
  }
  
  public QbFileHandler(File file) {
    this.byteStream = new ImprovedByteStream(file);
  }
  
  public ImprovedByteStream getByteStream() {
    return this.byteStream;
  }
  
  public boolean createTable() {
    this.fields = new HashMap<Integer, String>();
    this.byteStream.movePosition(-2);
    do {
    
    } while (readNextField());
    this.byteStream.reset();
    return true;
  }
  
  private boolean readNextField() {
    if (!this.byteStream.movePosition(2))
      return false; 
    byte[] ident = new byte[4];
    if (!this.byteStream.read(ident))
      return false; 
    byte[] figure = new byte[1];
    int stringLength = this.byteStream.getCountToFigure(figure);
    if (stringLength == -1)
      return false; 
    byte[] stringBytes = new byte[stringLength];
    this.byteStream.read(stringBytes);
    this.fields.put(Integer.valueOf(ByteBuffer.wrap(ident).getInt()), new String(stringBytes));
    return true;
  }
}
