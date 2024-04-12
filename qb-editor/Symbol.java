import java.util.Map;

public class Symbol implements Comparable<Symbol> {
  private Integer field;
  
  private String name;
  
  public Symbol(Map.Entry<Integer, String> entry) {
    this(entry.getValue(), entry.getKey());
  }
  
  public Symbol(String name, Integer field) {
    this.name = name;
    this.field = field;
  }
  
  public Integer getField() {
    return this.field;
  }
  
  public String getName() {
    return this.name;
  }
  
  public int compareTo(Symbol o) {
    return this.name.compareToIgnoreCase(o.getName());
  }
}
