package mcheli.hud;

import mcheli.reHud.MCH_Entity_Hud;
import mcheli.reHud.vec2;

public class MCH_HUDfixed extends MCH_HudItem{

	public DefineHudEntitiy FixedHud;

	/**
	 * ALL IMAGE PARAMETOR
	 */

	public vec2 positon=new vec2(0.5f,0.5f);

	public float rotation=0;

	public vec2 RotationPos=new vec2(0,0);

	public boolean isRotationPos=false;

	public vec2 size=new vec2(1,1);

	public String root_name="";

	public boolean isSetBrightnessMode=false;

	private boolean brightness=true;

	public MCH_Entity_Hud EntityHud=null;

    public MCH_HUDfixed(int fileLine,boolean brightness)
    {
        super(fileLine);
        this.isSetBrightnessMode=true;
        this.brightness=brightness;
    }


    public MCH_HUDfixed(int fileLine, DefineHudEntitiy fh,String  posx, String posy,String rot,String sizex,String sizey,String ...RotPos)
    {
        super(fileLine);
        this.FixedHud=fh;
        this.positon.x=tofloat(posx);
        this.positon.y=tofloat(posy);
        this.rotation=tofloat(rot);
        this.size.x=tofloat(sizex);
        this.size.y=tofloat(sizey);
        if(RotPos.length>0) {
        	this.isRotationPos=true;
        	this.RotationPos.x=tofloat(RotPos[0]);
        	this.RotationPos.y=tofloat(RotPos[1]);
        	this.rotation=tofloat(RotPos[2]);
        }
        if(fh instanceof DefineFixedhuds) {
        	this.root_name=((DefineFixedhuds) fh).parent.name;
        }
        if(fh instanceof DefineFixedhudGroup) {
        	this.root_name=((DefineFixedhudGroup) fh).DFH_LIST.get(0).parent.name;
        }
    }

    public float tofloat(String s) {
    	String o=this.toFormula(s);
    	return (float)this.calc(o);
    }

    public void execute(){
    	if(!this.FixedHud.IsCompletalyInited) {
    		this.FixedHud.final_init(this.mc);
    		if(this.FixedHud.IsCompletalyInitedok) {
    			this.FixedHud.IsCompletalyInited=true;
    			//MCH_Lib.Log("final_init="+this.FixedHud.name);
    		}
    	}
    	if(this.FixedHud.IsCompletalyInited) {
    		if(!this.isSetBrightnessMode) {
    			this.FixedHud.execute(this.size,this.positon,this.rotation,this.isRotationPos,this.RotationPos,this.mc);
    		}else if(this.EntityHud instanceof MCH_Entity_Hud){
    			this.EntityHud.SetLight(this.brightness);
    		}
    	}
    }

}
