package mcheli.hud;

import java.util.ArrayList;
import java.util.List;

public class MCH_FixedHudVariable extends MCH_HudItem {

    private List<MCH_HUDVariable> Variables=new ArrayList();

    public MCH_FixedHudVariable(int fileLine) {
        super(fileLine);
    }

    public void setV(MCH_HUDVariable value) {
    	this.Variables.add(value);
    }

    public void setActV(int index,String val) {
    	this.Variables.get(index).setVal(val);
    }

    public int isEqualValName(String name) {
    	int re=-1;
    	for(int i=0;i<this.Variables.size();i++) {
    		if(this.Variables.get(i).getName().equals(name)){
    			re=i;
    			break;
    		}
    	}
    	return re;
    }

    public void execute() {
    	for (int i=0;i<this.Variables.size();i++) {
    		if(this.Variables.get(i).getVal() instanceof String) {
                double d = calc(this.Variables.get(i).getVal());
                updateVarMapItem(this.Variables.get(i).getName(), d);
    		}
    	}
    }
}
