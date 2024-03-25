package mcheli.hud;

import java.util.ArrayList;
import java.util.List;

public class MCH_HudFunction extends MCH_HudItem {

	List<String> Argument;

	boolean useArgument=false;

	MCH_FixedHudVariable variables;

    public MCH_HudFunction(int fileLine,String data) {
        super(fileLine);
        this.Argument=new ArrayList();
    	String[] SplitedV=data.split(":");
    	for(int i=0;i<SplitedV.length;i++) {
    		this.Argument.add(SplitedV[i]);
    	}
    }

    public void setArgument(String Arg) {
    	this.useArgument=true;
    	this.Argument.add(Arg);
    }

	@Override
	public void execute() {
		// TODO 自動生成されたメソッド・スタブ

	}

}
