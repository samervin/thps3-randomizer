import java.nio.ByteBuffer;
import java.util.HashMap;
import java.util.Map;

public class QbParser {
  private ImprovedByteStream bs;

  private Map<Integer, String> fields;

  private StringBuffer output;

  private long pseudo = 0L;

  private String indent;

  private boolean elseIfPossible = false;

  private boolean breakLineAfterThis = false;

  public QbParser(ImprovedByteStream bs) {
    this.bs = bs;
    this.fields = new HashMap<Integer, String>();
  }

  public void setFields(Map<Integer, String> fields) {
    this.fields = fields;
  }

  public String parse() {
    this.pseudo = 1L;
    this.indent = "";
    this.output = new StringBuffer();
    do {

    } while (makeDecision());
    return this.output.toString();
  }

  public int getTablePosition() {
    this.output = new StringBuffer();
    do {

    } while (makeDecision());
    return this.bs.getPosition();
  }

  private boolean makeDecision() {
    boolean requestNewLineAfterNext = false;
    byte[] cmd = new byte[1];
    this.bs.read(cmd);
    switch (cmd[0]) {
      case 1:
        this.output.append("\n" + lineBegin());
        break;
      case 2:
        this.output.append("\n" + lineBegin(parseLong()));
        break;
      case 3:
        increaseNesting();
        this.output.append("STRUCT{\n" + lineBegin());
        this.breakLineAfterThis = false;
        break;
      case 4:
        decreaseNesting();
        this.output.append("}\n" + lineBegin());
        break;
      case 5:
        increaseNesting();
        this.output.append("ARRAY(\n" + lineBegin());
        break;
      case 6:
        decreaseNesting();
        this.output.append("\n" + lineBegin() + ")" + "\n" + lineBegin());
        break;
      case 7:
        this.output.append("= ");
        requestNewLineAfterNext = true;
        break;
      case 8:
        this.output.append("0x08 ");
        break;
      case 9:
        this.output.append("0x09 ");
        break;
      case 10:
        this.output.append("- ");
        break;
      case 11:
        this.output.append("+ ");
        break;
      case 12:
        this.output.append("/ ");
        break;
      case 13:
        this.output.append("* ");
        break;
      case 14:
        this.output.append("( ");
        break;
      case 15:
        this.output.append(") ");
        break;
      case 16:
        this.output.append("0x10 ");
        break;
      case 17:
        this.output.append("0x11 ");
        break;
      case 18:
        this.output.append("< ");
        break;
      case 19:
        this.output.append("<= ");
        break;
      case 20:
        this.output.append("> ");
        break;
      case 21:
        this.output.append(">= ");
        break;
      case 22:
        this.output.append(String.valueOf(parseField()) + " ");
        break;
      case 23:
        this.output.append(String.valueOf(parseLong()) + " ");
        break;
      case 24:
        this.output.append("0x18 ");
        break;
      case 25:
        this.output.append("0x19 ");
        break;
      case 26:
        this.output.append(String.valueOf(parseFloat()) + " ");
        break;
      case 27:
        this.output.append("\"" + parseString() + "\"" + " ");
        break;
      case 28:
        this.output.append("'" + parseString() + "'" + " ");
        break;
      case 29:
        this.output.append("0x1D ");
        break;
      case 30:
        this.output.append("VECTOR[" +
            parseFloat() + ";" + " " +
            parseFloat() + ";" + " " +
            parseFloat() + "]" + " ");
        break;
      case 31:
        this.output.append("PAIR[" +
            parseFloat() + ";" + " " +
            parseFloat() + "]" + " ");
        break;
      case 32:
        this.output.append("LOOP ");
        increaseNesting();
        break;
      case 33:
        this.output.delete(this.output.length() - 2, this.output.length());
        this.output.append("END LOOP ");
        decreaseNesting();
        break;
      case 34:
        this.output.append("BREAK\n" + lineBegin());
        break;
      case 35:
        this.output.append("FUNCTION ");
        increaseNesting();
        break;
      case 36:
        this.output.delete(this.output.length() - 2, this.output.length());
        this.output.append("END FUNCTION\n" + lineBegin());
        decreaseNesting();
        break;
      case 37:
        this.output.append("IF ");
        increaseNesting();
        break;
      case 38:
        this.output.delete(this.output.length() - 2, this.output.length());
        this.output.append("ELSE ");
        this.elseIfPossible = true;
        return true;
      case 39:
        this.output.append("0x23 ");
        break;
      case 40:
        this.output.delete(this.output.length() - 2, this.output.length());
        this.output.append("END IF ");
        decreaseNesting();
        break;
      case 41:
        this.output.append("RETURN ");
        break;
      case 42:
        this.output.append("0x2A ");
        break;
      case 44:
        this.output.append("NULL ");
        break;
      case 45:
        this.output.append("GLOBAL.");
        this.breakLineAfterThis = false;
        requestNewLineAfterNext = true;
        break;
      case 46:
        this.output.append("JUMP " + parseHex(4) + " ");
        break;
      case 47:
        this.output.append("RANDOM[" + parseRnd() + "]" + "\n" + lineBegin());
        break;
      case 48:
        this.output.append("0x30 ");
        break;
      case 49:
        this.output.append("0x31 ");
        break;
      case 50:
        this.output.append("OR ");
        break;
      case 51:
        this.output.append("AND ");
        break;
      case 52:
        this.output.append("0x34 ");
        break;
      case 53:
        this.output.append("0x35 ");
        break;
      case 54:
        this.output.append("0x36 ");
        break;
      case 55:
        // this.output.append("0x37 ");
        this.output.append("RAND3[" + parseRnd() + "]" + "\n" + lineBegin());
        break;
      case 56:
        this.output.append("0x38 ");
        break;
      case 57:
        this.output.append("NOT ");
        break;
      case 58:
        this.output.append("0x3A ");
        break;
      case 59:
        this.output.append("0x3B ");
        break;
      case 64:
        this.output.append("RAND2[" + parseRnd() + "]" + "\n" + lineBegin());
        break;
      case 43:
        return false;
    }
    if (this.breakLineAfterThis)
      this.output.append("\n" + lineBegin());
    this.breakLineAfterThis = false;
    if (requestNewLineAfterNext) {
      requestNewLineAfterNext = false;
      this.breakLineAfterThis = true;
    }
    this.elseIfPossible = false;
    return true;
  }

  private String parseField() {
    byte[] figure = new byte[4];
    this.bs.read(figure);
    Integer key = Integer.valueOf(ByteBuffer.wrap(figure).getInt());
    String name = this.fields.get(key);
    if (name == null) {
      name = "pseudo" + this.pseudo++;
      this.fields.put(key, name);
    }
    return name;
  }

  private long parseLong() {
    byte[] b = new byte[4];
    this.bs.read(b);
    byte[] b2 = new byte[4];
    b2[0] = b[3];
    b2[1] = b[2];
    b2[2] = b[1];
    b2[3] = b[0];
    return ByteBuffer.wrap(b2).getInt();
  }

  private float parseFloat() {
    byte[] b = new byte[4];
    this.bs.read(b);
    byte[] b2 = new byte[4];
    b2[0] = b[3];
    b2[1] = b[2];
    b2[2] = b[1];
    b2[3] = b[0];
    float value = ByteBuffer.wrap(b2).getFloat();
    return value;
  }

  private String parseString() {
    long stringLength = parseLong();
    byte[] stringBytes = new byte[(int)stringLength - 1];
    this.bs.read(stringBytes);
    this.bs.movePosition(1);
    return new String(stringBytes);
  }

  private String parseHex(int length) {
    byte[] b = new byte[length];
    this.bs.read(b);
    String value = "0x";
    for (int i = 0; i < length; i++) {
      String hex = Integer.toHexString(b[i] & 0xFF);
      while (hex.length() < 2)
        hex = "0" + hex;
      value = String.valueOf(value) + hex;
    }
    return value;
  }

  private String lineBegin() {
    return lineBegin(-1L);
  }

  private void increaseNesting() {
    if (this.elseIfPossible) {
      this.elseIfPossible = false;
    } else {
      this.indent = String.valueOf(this.indent) + "  ";
    }
  }

  private void decreaseNesting() {
    if (this.indent.length() > 1)
      this.indent = this.indent.substring(2);
  }

  private String lineBegin(long lineNumber) {
    if (lineNumber < 0L)
      return "        " + this.indent;
    return "#" + (String.valueOf(100000L + lineNumber) + "  " + this.indent).substring(1);
  }

  private String parseRnd() {
    String result = "";
    int count = (int)parseLong();
    result = String.valueOf(result) + count + "]" + "[";
    for (int i = 0; i < count; i++) {
      result = String.valueOf(result) + parseLong();
      if (i + 1 < count)
        result = String.valueOf(result) + "; ";
    }
    return result;
  }
}
