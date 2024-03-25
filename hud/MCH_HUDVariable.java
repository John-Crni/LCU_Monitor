package mcheli.hud;

public class MCH_HUDVariable {

	private String Name="";

	private String Val;

	public MCH_HUDVariable(String name) {
		this.Name=name;
	}

	public MCH_HUDVariable(String name,String val) {
		this.Name=name;
		this.Val=val;
	}


	public MCH_HUDVariable(MCH_HUDVariable clone) {
		this.Name=clone.getName();
		this.Val=clone.getVal();
	}

	public void setVal(String val) {
		this.Val=val;
	}

	public String getVal() {
		return this.Val;
	}

	public String getName() {
		return this.Name;
	}


}
