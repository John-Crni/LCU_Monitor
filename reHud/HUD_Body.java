package mcheli.reHud;

import java.util.List;

public class HUD_Body {

	private List<HUD> HUD_List;

	/**
	 *
	 * @param IdList
	 */
	public void createGroupedHud(int[] IdList) {
		int id1=0;
		int id2=0;
		
		if(IdList.length<2)return;
		
		for(int i=0;i<IdList.length;i++) {
			for(int j=0;j<this.HUD_List.size();j++) {
				
			}
		}

	}

	private void setNormSquare(Square S1,Square S2) {
		this.Trash.P2.setPos(new vec2(S1.P2.getPos().RvCompareXmax(S2.P2.getPos()),S1.P2.getPos().RvCompareYmax(S2.P2.getPos())));
		this.Trash.P4.setPos(new vec2(S1.P4.getPos().RvCompareXminVec(S2.P4.getPos()),S1.P4.getPos().RvCompareYminVec(S2.P4.getPos())));
		this.Trash.setSquareAuto();
	}

	private Square Trash=new Square();


}
