import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

public class ImprovedByteStream {
  private byte[] content;
  
  private int position = 0;
  
  public int getPosition() {
    return this.position;
  }
  
  public ImprovedByteStream(File file) {
    try {
      FileInputStream inputStream = new FileInputStream(file);
      this.content = new byte[(int)file.length()];
      inputStream.read(this.content);
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    } catch (IOException e) {
      e.printStackTrace();
    } 
  }
  
  public ImprovedByteStream(byte[] content) {
    this.content = content;
  }
  
  public int getLength() {
    return this.content.length;
  }
  
  public boolean searchFigure(byte[] figure) {
    return searchFigure(figure, true);
  }
  
  public boolean searchFigure(byte[] figure, boolean forward) {
    int initPosition = this.position;
    if (forward) {
      while (this.position + figure.length <= this.content.length) {
        if (isFigure(figure))
          return true; 
        this.position++;
      } 
    } else {
      while (this.position >= 0) {
        if (isFigure(figure))
          return true; 
        this.position--;
      } 
    } 
    this.position = initPosition;
    return false;
  }
  
  public boolean isFigure(byte[] figure) {
    return isFigure(figure, this.position);
  }
  
  public boolean isFigure(byte[] figure, int pos) {
    if (pos < 0)
      return false; 
    for (int i = 0; i < figure.length; i++) {
      if (pos >= this.content.length)
        return false; 
      if (figure[i] != this.content[pos])
        return false; 
      pos++;
    } 
    return true;
  }
  
  public boolean read(byte[] output) {
    int i = 0;
    while (i < output.length && this.position < this.content.length)
      output[i++] = this.content[this.position++]; 
    if (this.position == this.content.length)
      this.position = 0; 
    if (i + 1 < output.length)
      return false; 
    return true;
  }
  
  public boolean movePosition(int offset) {
    int test = this.position + offset;
    if (test < 0 || test >= this.content.length)
      return false; 
    this.position += offset;
    return true;
  }
  
  public int getCountToFigure(byte[] figure) {
    int initPosition = this.position;
    if (!searchFigure(figure))
      return -1; 
    int result = this.position - initPosition;
    this.position = initPosition;
    return result;
  }
  
  public void reset() {
    this.position = 0;
  }
}
