import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import javax.swing.ListModel;
import javax.swing.event.ListDataEvent;
import javax.swing.event.ListDataListener;

public class SymbolListModel implements ListModel {
  private List<ListDataListener> listDataListeners = new ArrayList<ListDataListener>();
  
  private List<Symbol> symbolList = new ArrayList<Symbol>();
  
  public void setFields(Map<Integer, String> fields) {
    int size = this.symbolList.size();
    this.symbolList.clear();
    Iterator<Map.Entry<Integer, String>> it = fields.entrySet().iterator();
    while (it.hasNext())
      this.symbolList.add(new Symbol(it.next())); 
    Collections.sort(this.symbolList);
    if (size < this.symbolList.size())
      size = this.symbolList.size(); 
    for (ListDataListener l : this.listDataListeners)
      l.contentsChanged(new ListDataEvent(this, 0, 0, size)); 
  }
  
  public void addListDataListener(ListDataListener l) {
    this.listDataListeners.add(l);
  }
  
  public Object getElementAt(int index) {
    return this.symbolList.get(index);
  }
  
  public int getSize() {
    return this.symbolList.size();
  }
  
  public void removeListDataListener(ListDataListener l) {
    this.listDataListeners.remove(l);
  }
  
  public void clear() {
    int size = this.symbolList.size();
    this.symbolList.clear();
    for (ListDataListener l : this.listDataListeners)
      l.contentsChanged(new ListDataEvent(this, 0, 0, size)); 
  }
  
  public void addField(Symbol s) {
    this.symbolList.add(s);
    Collections.sort(this.symbolList);
    for (ListDataListener l : this.listDataListeners)
      l.contentsChanged(new ListDataEvent(this, 0, 0, this.symbolList.size())); 
  }
}
