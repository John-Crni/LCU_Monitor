//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

package mcheli.hud;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import mcheli.MCH_BaseInfo;
import mcheli.MCH_Lib;
import mcheli.aircraft.MCH_EntityAircraft;
import mcheli.wrapper.W_ScaledResolution;
import net.minecraft.client.gui.ScaledResolution;
import net.minecraft.entity.player.EntityPlayer;

public class MCH_Hud extends MCH_BaseInfo {

    public static final MCH_Hud NoDisp = new MCH_Hud("none", "none");
    public final String name;
    public final String fileName;
    private List<MCH_HudItem> list;
    private List<MCH_HUDVariable> Vallist;
    private MCH_FixedHudVariable HudVariable;
    public boolean isWaitEndif;
    private boolean isDrawing;
    public boolean ishavefixedhud=false;
    public boolean isIfFalse;
    public boolean exit;

    public List<DefineHudEntitiy> fixedHudlist;
    public List<DefineHudEntitiy> executeFixedHudlist;//rootList

    public MCH_Hud(String name, String fname) {
        this.name = name;
        this.fileName = fname;
        this.list = new ArrayList();
        this.fixedHudlist=new ArrayList();
        this.executeFixedHudlist=new ArrayList();
        this.isDrawing = false;
        this.isIfFalse = false;
        this.exit = false;
    }

    public void checkData() {
        MCH_HudItem hud;
        for(Iterator i$ = this.list.iterator(); i$.hasNext(); hud.parent = this) {
            hud = (MCH_HudItem)i$.next();
        }

        if (this.isWaitEndif) {
            throw new RuntimeException("Endif not found!");
        }
    }

    public void setFixedHUDroot(){
         for(int i=0;i<this.list.size();i++) {
     		 if(this.list.get(i) instanceof MCH_HUDfixed) {
     			 MCH_HUDfixed item=(MCH_HUDfixed)this.list.get(i);
     			 if(item.root_name!="") {
     				this.executeFixedHudlist.add(this.getHudRoot(item.root_name));
     			 }


     		 }

     		 if(this.list.get(i) instanceof MCH_HudItemCall) {
     			 MCH_HudItemCall item=(MCH_HudItemCall)this.list.get(i);
     			 if(item.getName()==this.name) {
     				 break;
     			 }else {
     				 MCH_Hud hud = MCH_HudManager.get(item.getName());
     				 if(hud.ishavefixedhud) {
     					 List<DefineFixedhudRoot> re1=hud.getFixedHUDroot();
     					 for(int j=0;j<re1.size();j++) {
     						this.executeFixedHudlist.add(re1.get(j));
     					 }
     				 }
     			 }

     		 }

     	 }

     }

    public List<DefineFixedhudRoot> getFixedHUDroot(){
      	 List<DefineFixedhudRoot> re=new ArrayList();
      	 for(int i=0;i<this.list.size();i++) {
      		 if(this.list.get(i) instanceof MCH_HUDfixed) {
      			 MCH_HUDfixed item=(MCH_HUDfixed)this.list.get(i);
      			 if(item.root_name!="") {
      				re.add(this.getHudRoot(item.root_name));
      			 }


      		 }

      		 if(this.list.get(i) instanceof MCH_HudItemCall) {
      			 MCH_HudItemCall item=(MCH_HudItemCall)this.list.get(i);
      			 if(item.getName()==this.name) {
      				 break;
      			 }else {
      				 MCH_Hud hud = MCH_HudManager.get(item.getName());
      				 if(hud.ishavefixedhud) {
      					 List<DefineFixedhudRoot> re1=hud.getFixedHUDroot();
      					 for(int j=0;j<re1.size();j++) {
      						 re.add(re1.get(j));
      					 }
      				 }
      			 }

      		 }

      	 }

      	 return re;
      }

    public List<String> getFixedHUDrootname(){
   	 List<String> re=new ArrayList();
   	 for(int i=0;i<this.list.size();i++) {
   		 if(this.list.get(i) instanceof MCH_HUDfixed) {
   			 MCH_HUDfixed item=(MCH_HUDfixed)this.list.get(i);
   			 if(item.root_name!="") {
   				re.add(item.root_name);
   			 }


   		 }

   		 if(this.list.get(i) instanceof MCH_HudItemCall) {
   			 MCH_HudItemCall item=(MCH_HudItemCall)this.list.get(i);
   			 if(item.getName()==this.name) {
   				 break;
   			 }else {
   				 MCH_Hud hud = MCH_HudManager.get(item.getName());
   				 if(hud.ishavefixedhud) {
   					 List<String> re1=hud.getFixedHUDrootname();
   					 for(int j=0;j<re1.size();j++) {
   						 re.add(re1.get(j));
   					 }
   				 }
   			 }

   		 }

   	 }

   	 return re;
   }

    public List<String> getFixedHUDname(){
    	 List<String> re=new ArrayList();
    	 for(int i=0;i<this.list.size();i++) {
    		 if(this.list.get(i) instanceof MCH_HUDfixed) {
    			 MCH_HUDfixed item=(MCH_HUDfixed)this.list.get(i);
    			 re.add(item.FixedHud.name);

    		 }

    		 if(this.list.get(i) instanceof MCH_HudItemCall) {
    			 MCH_HudItemCall item=(MCH_HudItemCall)this.list.get(i);
    			 if(item.getName()==this.name) {
    				 break;
    			 }else {
    				 MCH_Hud hud = MCH_HudManager.get(item.getName());
    				 if(hud.ishavefixedhud) {
    					 List<String> re1=hud.getFixedHUDname();
    					 for(int j=0;j<re1.size();j++) {
    						 re.add(re1.get(j));
    					 }
    				 }
    			 }

    		 }

    	 }

    	 return re;
    }

    public DefineFixedhudRoot getHudRoot(String rootName) {
    	DefineFixedhudRoot item=null;
      	 for(int i=0;i<this.fixedHudlist.size();i++) {
		 if(this.fixedHudlist.get(i) instanceof DefineFixedhudRoot) {
			 item=(DefineFixedhudRoot)this.fixedHudlist.get(i);
			 if(item.name.equalsIgnoreCase(rootName)) {
				 break;
			 }else {
				 item=null;
			 }
		}
   	 }
      	return item;
    }

    int hudList_counter=0;

    int fixedhud_counter=0;

    public void loadItemData(int fileLine, String item, String data) {
        String[] prm = data.split("\\s*,\\s*");

        if (prm != null && prm.length != 0) {
            if (item.equalsIgnoreCase("If")) {
                if (this.isWaitEndif) {
                    throw new RuntimeException("Endif not found!");
                }

                this.list.add(new MCH_HudItemConditional(fileLine, false, prm[0]));
               // MCH_Lib.Log("SUCSESS2!"+prm[0]);
                this.isWaitEndif = true;
            } else if (item.equalsIgnoreCase("Endif")) {
                if (!this.isWaitEndif) {
                    throw new RuntimeException("IF in a pair can not be found!");
                }

                this.list.add(new MCH_HudItemConditional(fileLine, true, ""));
                this.isWaitEndif = false;
            } else {
                String rot;
                if (!item.equalsIgnoreCase("DrawString") && !item.equalsIgnoreCase("DrawCenteredString")) {
                    if (item.equalsIgnoreCase("Exit")) {
                        this.list.add(new MCH_HudItemExit(fileLine));
                    } else if (item.equalsIgnoreCase("Color")) {
                        MCH_HudItemColor c;
                        if (prm.length == 1) {
                            c = MCH_HudItemColor.createByParams(fileLine, new String[]{prm[0]});
                            if (c != null) {
                                this.list.add(c);
                            }
                        } else if (prm.length == 4) {
                            String[] s = new String[]{prm[0], prm[1], prm[2], prm[3]};
                            c = MCH_HudItemColor.createByParams(fileLine, s);
                            if (c != null) {
                                this.list.add(c);
                            }
                        }
                    } else if (item.equalsIgnoreCase("DrawTexture")) {
                        if (prm.length >= 9 && prm.length <= 10) {
                            rot = prm.length == 10 ? prm[9] : "0";
                            this.list.add(new MCH_HudItemTexture(fileLine, prm[0], prm[1], prm[2], prm[3], prm[4], prm[5], prm[6], prm[7], prm[8], rot));
                        }
                    }
                    else if (item.equalsIgnoreCase("DrawBombSight"))
                    {
                        if (prm.length >= 9 && prm.length <= 10)
                        {
                        	String type= prm.length == 10 ? prm[9] : "0";
                            //type = prm.length == 10 ? prm[9] : "0";
                            this.list.add(new MCH_HudItemBombSight(fileLine, prm[0], prm[1], prm[2], prm[3], prm[4], prm[5], prm[6], prm[7], prm[8], type));
                        }
                    }
                    else if (item.equalsIgnoreCase("DrawBulletSight"))
                    {
                        if (prm.length >= 9 && prm.length <= 10)
                        {
                        	String type= prm.length == 10 ? prm[9] : "0";
                            //type = prm.length == 10 ? prm[9] : "0";
                            this.list.add(new MCH_HudItemBulletSight(fileLine, prm[0], prm[1], prm[2], prm[3], prm[4], prm[5], prm[6], prm[7], prm[8], type));
                        }
                    }
                    else if (item.equalsIgnoreCase("DrawFixedTexture"))
                    {
                        if (prm.length >= 9 && prm.length <= 10)
                        {
                        	//String type= prm.length == 10 ? prm[9] : "0";
                        	rot = prm.length == 10 ? prm[9] : "0";
                            this.list.add(new drawFixedTexture(fileLine, prm[0], prm[1], prm[2], prm[3], prm[4], prm[5], prm[6], prm[7], prm[8], rot));
                        }
                    }
                    else if (item.equalsIgnoreCase("DrawTextureByScleenSize"))
                    {
                        if (prm.length >= 9 && prm.length <= 10)
                        {
                        	//String type= prm.length == 10 ? prm[9] : "0";
                        	rot = prm.length == 10 ? prm[9] : "0";
                           // this.list.add(new MCH_HudItemTSS(fileLine, prm[0], prm[1], prm[2], prm[3], prm[4], prm[5], prm[6], prm[7], prm[8], rot));
                        }

                    }
                    else if(item.equalsIgnoreCase("Variable")){
                    	if (!(this.HudVariable instanceof MCH_FixedHudVariable)) {
                    		this.HudVariable=new MCH_FixedHudVariable(fileLine);
                    	}

                    	for(int i=0;i<prm.length;i++) {
                    		this.HudVariable.setV(new MCH_HUDVariable(prm[i]));
                    		//MCH_Lib.Log("[V+"+i+"]="+prm[i]);
                    		this.list.add(this.HudVariable);
                    	}
                    }

                    else if (item.equalsIgnoreCase("FixedHudRoot"))
                    {
                        if (prm.length >= 3 && prm.length <= 6)
                        {
                        	String sizex=prm.length<5?"1":prm[4];
                        	String sizey=prm.length<6?"1":prm[5];

                            double[][] coords={{0,0,0},{0,0,0},{0,0,0},{0,0,0}};
                            int vec2Num=0;

                            for(int i=0;i<prm.length;i++){
                                prm[i]=prm[i].toLowerCase();
                                if(prm[i].contains("vec3(")){
                                    vec2Num+=1;
                                }
                            }

                            if(vec2Num==4){
                            	int m=0;
                                for(int i=0;i<prm.length;i++){
                                    if(prm[i].contains("vec3")){
                                        prm[i]=prm[i].replace("vec3", "").replace("(", "").replace(")", "");
                                        String[] dannneza=prm[i].split(":");
                                        coords[m][0]=Double.parseDouble(dannneza[0]);
                                        coords[m][1]=Double.parseDouble(dannneza[1]);
                                        coords[m][2]=Double.parseDouble(dannneza[2]);
                                        m+=1;
                                    }
                                }
                                MCH_Lib.Log("this.fixedHudlist");
                            	this.fixedHudlist.add(new DefineFixedhudRoot(this.setHudName(prm[0]),coords));
                            	hudList_counter+=1;
                            }else {
                            	MCH_Lib.Log("this.fixedHudlist");
                            	this.fixedHudlist.add(new DefineFixedhudRoot(this.setHudName(prm[0]), prm[1], prm[2], prm[3],sizex, sizey));
                            	hudList_counter+=1;
                            }
                        }
                    }

                    else if (item.equalsIgnoreCase("FixedHud"))
                    {//Name,RootName,Pos,Size,texName,rotation

                        if (prm.length >= 7 && prm.length <= 8&& hudList_counter>0)
                        {
                        	MCH_Lib.Log("FixedHud");

                        	String rotation=prm.length<8?"0":prm[7];

                        	String root_name=prm[1];
                        	int size=this.fixedHudlist.size();
                        	DefineFixedhudRoot DFR = null;

                        	for(int i=0;i<size;i++) {
                        		DFR=(DefineFixedhudRoot)this.fixedHudlist.get(i);
                        		if(this.isEqualhudNames(DFR.name, root_name))break;
                        	}
                        	//String n,DefineFixedhudRoot dfr,String x,String y,String sizex,String sizey,String TexName,String rot
                        	this.fixedHudlist.add(new DefineFixedhuds(this.setHudName(prm[0]),DFR,prm[2], prm[3],  prm[4], prm[5],prm[6], rotation));
//String n,DefineFixedhudRoot dfr,String x,String y,String sizex,String sizey,String TexName,String rot) {
                        	this.ishavefixedhud=true;
                        	fixedhud_counter+=1;

                        	MCH_Lib.Log("FixedHudEnd");
                        }
                    }

                    else if (item.equalsIgnoreCase("FixedHudGroupe"))
                    {//Name,RootName,Pos,Size,texName,rotation

                        if (prm.length >=3&& fixedhud_counter>=(prm.length-1))
                        {
                        	//MCH_Lib.Log("GROUPE2!!");
                        	String fixhudName="";
                        	List<DefineFixedhuds> HUD_LIST= new ArrayList();

                        	//DefineFixedhuds Trash=null;
                        	for(int i=1;i<prm.length;i++) {
                        		fixhudName=prm[i];
                        		for(int j=0;j<this.fixedHudlist.size();j++) {
                        			DefineHudEntitiy Trash=(DefineHudEntitiy) this.fixedHudlist.get(j);
                        			if((this.isEqualhudNames(Trash.name, fixhudName)) &&  Trash instanceof DefineFixedhuds) {
                        				//MCH_Lib.Log("GROUPE2!!:"+Trash.name);
                        				HUD_LIST.add((DefineFixedhuds) Trash);
                        				break;
                        			}
                        		}

                        	}
                        	this.fixedHudlist.add(new DefineFixedhudGroup(this.setHudName(prm[0]),HUD_LIST));
                        }
                    }
                    else if (item.equalsIgnoreCase("DrawRect")) {
                        if (prm.length == 4) {
                            this.list.add(new MCH_HudItemRect(fileLine, prm[0], prm[1], prm[2], prm[3]));
                        }
                    } else {
                        int len;
                        if (item.equalsIgnoreCase("DrawLine")) {
                            len = prm.length;
                            if (len >= 4 && len % 2 == 0) {
                                this.list.add(new MCH_HudItemLine(fileLine, prm));
                            }
                        } else if (item.equalsIgnoreCase("DrawLineStipple")) {
                            len = prm.length;
                            if (len >= 6 && len % 2 == 0) {
                                this.list.add(new MCH_HudItemLineStipple(fileLine, prm));
                            }
                        } else if (item.equalsIgnoreCase("Call")) {
                            len = prm.length;
                            if (len == 1) {
                                this.list.add(new MCH_HudItemCall(fileLine, prm[0]));
                            }
                        } else if (!item.equalsIgnoreCase("DrawEntityRadar") && !item.equalsIgnoreCase("DrawEnemyRadar")) {
                            if (!item.equalsIgnoreCase("DrawGraduationYaw") && !item.equalsIgnoreCase("DrawGraduationPitch1") && !item.equalsIgnoreCase("DrawGraduationPitch2") && !item.equalsIgnoreCase("DrawGraduationPitch3")) {
                                if (item.equalsIgnoreCase("DrawCameraRot") && prm.length == 2) {
                                    this.list.add(new MCH_HudItemCameraRot(fileLine, prm[0], prm[1]));
                                }
                            } else if (prm.length == 4) {
                                int type = -1;
                                if (item.equalsIgnoreCase("DrawGraduationYaw")) {
                                    type = 0;
                                }

                                if (item.equalsIgnoreCase("DrawGraduationPitch1")) {
                                    type = 1;
                                }

                                if (item.equalsIgnoreCase("DrawGraduationPitch2")) {
                                    type = 2;
                                }

                                if (item.equalsIgnoreCase("DrawGraduationPitch3")) {
                                    type = 3;
                                }

                                this.list.add(new MCH_HudItemGraduation(fileLine, type, prm[0], prm[1], prm[2], prm[3]));
                            }
                        } else if (prm.length == 5) {
                            this.list.add(new MCH_HudItemRadar(fileLine, item.equalsIgnoreCase("DrawEntityRadar"), prm[0], prm[1], prm[2], prm[3], prm[4]));
                        }
                    }
                } else if (prm.length >= 3) {
                    rot = prm[2];
                    if (rot.charAt(0) == '"' && rot.charAt(rot.length() - 1) == '"') {
                        rot = rot.substring(1, rot.length() - 1);
                        this.list.add(new MCH_HudItemString(fileLine, prm[0], prm[1], rot, prm, item.equalsIgnoreCase("DrawCenteredString")));
                    }
                } if(this.HudVariable instanceof MCH_FixedHudVariable){
                	String val=prm[0];
                	boolean getImpactPosMode=false;
                	boolean getImpactPosModeX=false;
                	boolean getImpactPosModeY=false;
                	boolean getImpactPosModeZ=false;
                	boolean getHudPosMode=false;
                	boolean getHudPosModeX=false;
                	boolean getHudPosModeY=false;
                	boolean getHudPosModeZ=false;
                	val=val.toLowerCase();
                	if(val.contains("getbulletimpactpos()")) {
                		getImpactPosMode=true;
                		if(val.contains("->")) {
                			if(val.equalsIgnoreCase("getbulletimpactpos()->x")) {
                				getImpactPosModeX=true;
                			}
                			if(val.equalsIgnoreCase("getbulletimpactpos()->y")) {
                				getImpactPosModeY=true;
                			}
                			if(val.equalsIgnoreCase("getbulletimpactpos()->z")) {
                				getImpactPosModeZ=true;
                			}
                		}
                	}else if(this.fixedHudlist.size()>=2&&val.contains("->getHudPos(")) {
                    	String[] splited = val.split("->");
                    	String Initial=splited[0];
                    	for(int i=0;i<this.fixedHudlist.size();i++) {//探す
                    		if(this.isEqualhudNames(this.fixedHudlist.get(i).name, Initial)) {
                        		String pos=val.replace(Initial,"").replace("->getHudPos", "").replace("(", "").replace(")","");
                        		String[] posdata=val.split(":");
                    			if(posdata.length==3) {//position のみ
                    				String[] re={"0","0","0"};
                    				re[0]=posdata[0];
                    				re[1]=posdata[1];
                    				re[2]=posdata[2];
                    				}
                        			this.list.add(new MCH_Hudgethudpos(fileLine,item,,this.fixedHudlist.get(i)));
                    			}
                    	}
                	}


                	String[] SplitedV=item.split(",");
                	int index=this.HudVariable.isEqualValName(item);

                	if(index!=-1) {
                		MCH_Lib.Log("[Vopo]="+val);
                		this.HudVariable.setActV(index, val);
                	}
                }

                if(this.fixedHudlist.size()>=2&&item.toLowerCase().contains("->update")&&prm.length>=2) {//?????->update=position.rotation,size

                	boolean isRotationUpdate=false;
                	boolean isBrightnessUpdate=false;
                	if(item.toLowerCase().contains("->update->rotation")) {
                		isRotationUpdate=true;
                	}
                   	if(item.toLowerCase().contains("->update->brightness")) {
                   		isBrightnessUpdate=true;
                	}

                	String[] splited = item.split("->");
                	String Initial=splited[0].toLowerCase();
                	for(int i=0;i<this.fixedHudlist.size();i++) {//探す

                		if(this.isEqualhudNames(this.fixedHudlist.get(i).name, Initial)&&isRotationUpdate) {
                			if(prm.length==3) {//position のみ
                				String[] re={"1","2","3"};
                				re[0]=prm[0];
                				re[1]=prm[1];
                				re[2]=prm[2];
                				this.list.add(new MCH_HUDfixed(fileLine,this.fixedHudlist.get(i),"0.5","0.5","0","1","1",re));//Pos,rot,size,rotation
                				this.setFIxed2Root((MCH_HUDfixed)this.list.get(this.list.size()-1));
                			}
                		}else if(this.isEqualhudNames(this.fixedHudlist.get(i).name, Initial)&&isBrightnessUpdate) {
                			if(prm.length==1) {//position のみ
                				boolean brightness=true;
                				if(prm[0].equalsIgnoreCase("on")) {
                					brightness=true;
                				}else if (prm[0].equalsIgnoreCase("off")) {
                					brightness=false;
                				}
                				this.list.add(new MCH_HUDfixed(fileLine,brightness));
                				//this.setFIxed2Root((MCH_HUDfixed)this.list.get(this.list.size()-1));
                			}
                		}else if(this.isEqualhudNames(this.fixedHudlist.get(i).name, Initial)) {
                			if(prm.length<=2) {//position のみ
                				this.list.add(new MCH_HUDfixed(fileLine,this.fixedHudlist.get(i),prm[0],prm[1],"0","1","1"));
                				this.setFIxed2Root((MCH_HUDfixed)this.list.get(this.list.size()-1));
                			}
                			if(prm.length==3) {//position のみ
                				this.list.add(new MCH_HUDfixed(fileLine,this.fixedHudlist.get(i),prm[0],prm[1],prm[2],"1","1"));
                				this.setFIxed2Root((MCH_HUDfixed)this.list.get(this.list.size()-1));
                			}
                			if(prm.length>3&&prm.length<=5) {//position のみ
                				this.list.add(new MCH_HUDfixed(fileLine,this.fixedHudlist.get(i),prm[0],prm[1],prm[2],prm[3],prm[4]));
                				this.setFIxed2Root((MCH_HUDfixed)this.list.get(this.list.size()-1));
                			}

                		}

                	}

                }


            }

        }
    }

    private void setFIxed2Root(MCH_HUDfixed hud) {
    	if(hud.root_name!="") {
    		DefineFixedhudRoot Root=this.getHudRoot(hud.root_name);
    		Root.fixedHudlist.add(hud);
    	}
    }

    private boolean isEqualhudNames(String parent,String n2) {
    	boolean re=false;
    	String[] split = parent.split("->");
    	if(split[1].equalsIgnoreCase(n2)) {
    		re=true;
    	}
    	return re;
    }
    

    private String setHudName(String name) {
    	return (this.name+"->"+name);
    }

    public void draw(MCH_EntityAircraft ac, EntityPlayer player, float partialTicks) {
        MCH_HudItem.ac = ac;
        MCH_HudItem.player = player;
        MCH_HudItem.partialTicks = partialTicks;
        ScaledResolution scaledresolution = new W_ScaledResolution(MCH_HudItem.mc,MCH_HudItem.mc.displayWidth,MCH_HudItem.mc.displayHeight);
        MCH_HudItem.scaleFactor = scaledresolution.getScaleFactor();
        if (MCH_HudItem.scaleFactor <= 0) {
            MCH_HudItem.scaleFactor = 1;
        }

        MCH_HudItem.width = (double)MCH_HudItem.mc.displayWidth / (double)MCH_HudItem.scaleFactor;
        MCH_HudItem.height = (double)MCH_HudItem.mc.displayHeight / (double)MCH_HudItem.scaleFactor;
        MCH_HudItem.centerX = MCH_HudItem.width / 2.0D;
        MCH_HudItem.centerY = MCH_HudItem.height / 2.0D;
        this.isIfFalse = false;
        this.isDrawing = false;
        this.exit = false;
        if (ac != null && ac.getAcInfo() != null && player != null) {
            MCH_HudItem.update();
            this.drawItems();
            MCH_HudItem.drawVarMap();
        }

    }


    protected void drawItems() {
        if (!this.isDrawing) {
            this.isDrawing = true;
            Iterator i$ = this.list.iterator();

            while(i$.hasNext()) {
                MCH_HudItem hud = (MCH_HudItem)i$.next();
                byte line = -1;

                try {
                    int line1 = hud.fileLine;

                    if (hud.canExecute()) {
                        hud.execute();
                        if (this.exit) {
                            break;
                        }
                    }
                } catch (Exception var5) {
                    MCH_Lib.Log("#### Draw HUD Error!!!: line=%d, file=%s", new Object[]{Integer.valueOf(line), this.fileName});
                    var5.printStackTrace();
                    throw new RuntimeException(var5);
                }
            }

            this.exit = false;
            this.isIfFalse = false;
            this.isDrawing = false;
        }

    }
}
