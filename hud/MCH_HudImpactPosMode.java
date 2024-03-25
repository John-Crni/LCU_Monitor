package mcheli.hud;

import net.minecraft.util.Vec3;

public class MCH_HudImpactPosMode extends MCH_HudFunction{

	boolean modeX=false;

	boolean modeY=false;

	boolean modeZ=false;

	PreEAClass peac=null;

	Vec3 Vec;

    public MCH_HudImpactPosMode(int fileLine,String data) {
        super(fileLine,data);
        this.peac=new PreEAClass();
    }

	@Override
	public void execute() {
		this.Vec=this.peac.getLandInDistance(player,this.Altitude+250,ac);
    	for (int i=0;i<this.Argument.size();i++) {
    		if(this.Argument.get(i) instanceof String) {
    			switch(i) {
    				case 1:updateVarMapItem(this.Argument.get(i), this.Vec.xCoord);break;
    				case 2:updateVarMapItem(this.Argument.get(i), this.Vec.yCoord);break;
    				case 3:updateVarMapItem(this.Argument.get(i), this.Vec.zCoord);break;
    			}
    		}
    	}
	}

}
