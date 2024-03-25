package mcheli.hud;

import mcheli.eval.eval.ExpRuleFactory;
import mcheli.eval.eval.Expression;
import mcheli.eval.eval.var.MapVariable;
import mcheli.reHud.HudSquare;
import mcheli.reHud.vec2;
import net.minecraft.client.Minecraft;

public abstract class DefineHudEntitiy {

	public String name;

	public boolean IsCompletalyInited=false;

	public boolean IsCompletalyInitedok=false;

	public HudSquare ExecuteFunc;


	public DefineHudEntitiy(String n) {
		this.name=n;
	}

    public static String toFormula(String s) {
        return s.toLowerCase().replaceAll("#", "0x").replace("\t", " ").replace(" ", "");
    }

    public static double calc(String s) {
        Expression exp = ExpRuleFactory.getDefaultRule().parse(s);

        exp.setVariable(new MapVariable(MCH_HudItem.varMap));
        return exp.evalDouble();
    }

    public float tofloat(String s) {
    	String o=this.toFormula(s);
    	return (float)this.calc(o);
    }

    public void final_init(Minecraft mc) {

    }

	public void execute(vec2 size,vec2 pos,float rot, boolean isrotvec,vec2 rotvec1,Minecraft mc) {

	}

	public void UpdateBrightness(boolean onoff) {

	}


}
