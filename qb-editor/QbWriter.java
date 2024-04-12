import java.awt.Dialog;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import javax.swing.JProgressBar;

public class QbWriter implements Runnable {
  private ByteArrayOutputStream os;

  private String input;

  private Map<String, Integer> fieldMap;

  private int pos;

  private boolean unmarkedNumbers = false;

  private String test;

  private File output;

  private boolean isRunning = false;

  private JProgressBar progress = null;

  private Dialog owner;

  public QbWriter(String input, File output, Map<Integer, String> fields) {
    this.os = new ByteArrayOutputStream();
    this.input = input;
    this.output = output;
    this.fieldMap = new HashMap<String, Integer>();
    Iterator<Map.Entry<Integer, String>> it = fields.entrySet().iterator();
    while (it.hasNext()) {
      Map.Entry<Integer, String> pair = it.next();
      this.fieldMap.put(pair.getValue(), pair.getKey());
    }
  }

  public void run() {
    this.pos = 0;
    this.isRunning = true;
    try {
      do {

      } while (nextToken() && this.isRunning);
      if (this.isRunning) {
        createFieldsTable();
        FileOutputStream fos = new FileOutputStream(this.output);
        fos.write(this.os.toByteArray());
        fos.close();
      }
    } catch (Exception e) {
      e.printStackTrace();
    }
    this.isRunning = false;
  }

  public void cancel() {
    this.isRunning = false;
  }

  public void setOwner(Dialog owner) {
    this.owner = owner;
  }

  public void setProgressBar(JProgressBar progress) {
    this.progress = progress;
    progress.setMinimum(0);
    progress.setMaximum(this.input.length());
  }

  private boolean nextToken() throws IOException {
    if (this.progress != null) {
      this.progress.setValue(this.pos);
      this.progress.repaint();
    }
    while (this.pos < this.input.length() && (this.input.charAt(this.pos) == '\n' || this.input.charAt(this.pos) == ' '))
      this.pos++;
    if (this.pos >= this.input.length())
      return false;
    if (this.input.length() > this.pos + 40) {
      this.test = this.input.substring(this.pos, this.pos + 40);
    } else {
      this.test = this.input.substring(this.pos, this.input.length());
    }
    if (this.test.indexOf("IF", 0) == 0) {
      command("IF", 37);
    } else if (this.test.indexOf("ELSE", 0) == 0) {
      command("ELSE", 38);
    } else if (this.test.indexOf("END IF", 0) == 0) {
      command("END IF", 40);
    } else if (this.test.indexOf("NOT", 0) == 0) {
      command("NOT", 57);
    } else if (this.test.indexOf("AND", 0) == 0) {
      command("AND", 51);
    } else if (this.test.indexOf("OR", 0) == 0) {
      command("OR", 50);
    } else if (this.test.indexOf("<=", 0) == 0) {
      command("<=", 19);
    } else if (this.test.indexOf(">=", 0) == 0) {
      command(">=", 21);
    } else if (this.test.indexOf("<", 0) == 0) {
      command("<", 18);
    } else if (this.test.indexOf(">", 0) == 0) {
      command(">", 20);
    } else if (this.test.indexOf("=", 0) == 0) {
      command("=", 7);
    } else if (this.test.indexOf("+", 0) == 0) {
      command("+", 11);
    } else if (this.test.indexOf("/", 0) == 0) {
      command("/", 13);
    } else if (this.test.indexOf("*", 0) == 0) {
      command("*", 12);
    } else if (this.test.indexOf("FUNCTION", 0) == 0) {
      command("FUNCTION", 35);
    } else if (this.test.indexOf("END FUNCTION", 0) == 0) {
      command("END FUNCTION", 36);
    } else if (this.test.indexOf("LOOP", 0) == 0) {
      command("LOOP", 32);
    } else if (this.test.indexOf("END LOOP", 0) == 0) {
      command("END LOOP", 33);
    } else if (this.test.indexOf("BREAK", 0) == 0) {
      command("BREAK", 34);
    } else if (this.test.indexOf("RETURN", 0) == 0) {
      command("RETURN", 41);
    } else if (this.test.indexOf("JUMP", 0) == 0) {
      command("JUMP", 46);
    } else if (this.test.indexOf("NULL", 0) == 0) {
      command("NULL", 44);
    } else if (this.test.indexOf("ARRAY", 0) == 0) {
      command("ARRAY", 5);
    } else if (this.test.indexOf("VECTOR", 0) == 0) {
      command("VECTOR", 30);
    } else if (this.test.indexOf("PAIR", 0) == 0) {
      command("PAIR", 31);
    } else if (this.test.indexOf("STRUCT", 0) == 0) {
      command("STRUCT", 3);
    } else if (this.test.indexOf("RANDOM", 0) == 0) {
      command("RANDOM", 47);
    } else if (this.test.indexOf("RAND2", 0) == 0) {
      command("RAND2", 64);
    } else if (this.test.indexOf("RAND3", 0) == 0) {
      command("RAND3", 55);
    } else if (this.test.indexOf("GLOBAL.", 0) == 0) {
      command("GLOBAL.", 45);
    } else if (this.test.indexOf("(", 0) == 0) {
      command("(");
    } else if (this.test.indexOf(")", 0) == 0) {
      command(")", 6);
    } else if (this.test.indexOf("[", 0) == 0) {
      command("[");
      this.unmarkedNumbers = true;
    } else if (this.test.indexOf("]", 0) == 0) {
      command("]");
      this.unmarkedNumbers = false;
    } else if (this.test.indexOf("{", 0) == 0) {
      command("{");
    } else if (this.test.indexOf("}", 0) == 0) {
      command("}", 4);
    } else if (this.test.indexOf(";", 0) == 0) {
      command(";");
    } else if (this.test.indexOf("\"", 0) == 0) {
      this.os.write(parseString((byte)27, "\""));
    } else if (this.test.indexOf("'", 0) == 0) {
      this.os.write(parseString((byte)28, "'"));
    } else if (this.test.indexOf("#", 0) == 0) {
      this.os.write(2);
      this.os.write(parseLong(extractTokenAt(++this.pos)));
    } else if (this.test.indexOf("0x", 0) == 0) {
      this.os.write(parseHex(extractTokenAt(this.pos)));
    } else if (extractTokenAt(this.pos).matches("[-+]?[0-9]*\\.[0-9]+([eE][-+]?[0-9]+)?")) {
      if (!this.unmarkedNumbers)
        this.os.write(26);
      this.os.write(parseFloat(extractTokenAt(this.pos)));
    } else if (extractTokenAt(this.pos).matches("[-+]?[0-9]*")) {
      if (!this.unmarkedNumbers)
        this.os.write(23);
      this.os.write(parseLong(extractTokenAt(this.pos)));
    } else if (this.test.indexOf("-", 0) == 0) {
      command("-", 10);
    } else {
      this.os.write(parseField(extractTokenAt(this.pos)));
    }
    return true;
  }

  private void command(String word) {
    this.pos += word.length();
  }

  private void command(String word, int b) {
    command(word);
    this.os.write(b);
  }

  private String extractTokenAt(int pos) {
    String token = "";
    if ("-0123456789".indexOf(this.input.charAt(pos)) == -1) {
      while (this.input.charAt(pos) != ' ' && this.input.charAt(pos) != '\n' && this.input.indexOf(";", pos) != pos)
        token = String.valueOf(token) + this.input.charAt(pos++);
    } else if (this.test.indexOf("0x", 0) == 0) {
      while ("0123456789xabcdef".indexOf(this.input.charAt(pos)) != -1)
        token = String.valueOf(token) + this.input.charAt(pos++);
    } else {
      while ("-0123456789.E".indexOf(this.input.charAt(pos)) != -1)
        token = String.valueOf(token) + this.input.charAt(pos++);
    }
    return token;
  }

  private byte[] parseLong(String value) {
    int number = Integer.parseInt(value);
    byte[] b = new byte[4];
    byte[] b2 = ByteBuffer.wrap(new byte[4]).putInt(number).array();
    b[0] = b2[3];
    b[1] = b2[2];
    b[2] = b2[1];
    b[3] = b2[0];
    this.pos += value.length();
    return b;
  }

  private byte[] parseFloat(String value) {
    float number = Float.parseFloat(value);
    byte[] b = new byte[4];
    byte[] b2 = ByteBuffer.wrap(new byte[4]).putFloat(number).array();
    b[0] = b2[3];
    b[1] = b2[2];
    b[2] = b2[1];
    b[3] = b2[0];
    this.pos += value.length();
    return b;
  }

  private byte[] parseHex(String value) {
    byte[] result = new byte[value.length() / 2 - 1];
    for (int pointer = 2; pointer + 1 < value.length(); pointer += 2) {
      String hexByte = value.substring(pointer, pointer + 2);
      result[(pointer - 2) / 2] =
        (byte)((Character.digit(hexByte.charAt(0), 16) << 4) +
        Character.digit(hexByte.charAt(1), 16));
    }
    this.pos += value.length();
    return result;
  }

  private byte[] parseString(byte marker, String representation) {
    int start = ++this.pos;
    int end = -1;
    boolean endFound = false;
    while (!endFound) {
      if (this.input.charAt(this.pos) == representation.charAt(0))
        endFound = true;
      this.pos++;
    }
    end = this.pos - 1;
    ByteBuffer result = ByteBuffer.wrap(new byte[end - start + 6]);
    result.put(marker);
    int oldPos = this.pos;
    result.put(parseLong(Long.toString((end - start + 1))));
    this.pos = oldPos;
    result.put(this.input.substring(start, end).getBytes());
    result.put((byte)0);
    return result.array();
  }

  private Integer crc32(String value) {
    return Integer.valueOf(CRCGenerator.generateCRC(value));
  }

  private byte[] parseField(String value) {
    byte[] result = new byte[5];
    if (!this.fieldMap.containsKey(value))
      this.fieldMap.put(value, crc32(value));
    result = ByteBuffer.wrap(result).put((byte)22).putInt(((Integer)this.fieldMap.get(value)).intValue()).array();
    this.pos += value.length();
    return result;
  }

  private void createFieldsTable() throws IOException {
    Iterator<Map.Entry<String, Integer>> it = this.fieldMap.entrySet().iterator();
    while (it.hasNext()) {
      Map.Entry<String, Integer> pair = it.next();
      this.os.write(43);
      this.os.write(ByteBuffer.wrap(new byte[4]).putInt(((Integer)pair.getValue()).intValue()).array());
      this.os.write(((String)pair.getKey()).getBytes());
      this.os.write(0);
    }
    this.os.write(0);
  }
}
