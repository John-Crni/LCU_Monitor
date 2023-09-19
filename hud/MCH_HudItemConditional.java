package mcheli.hud;

public class MCH_HudItemConditional extends MCH_HudItem {

    private final boolean isEndif;
    private final String conditional;

    public MCH_HudItemConditional(int fileLine, boolean isEndif, String conditional) {
        super(fileLine);
        this.isEndif = isEndif;
        this.conditional = conditional;
        //MCH_Lib.Log("THIS_CONDITIONAL"+this.conditional);

    }

   // public boolean canExecute() { 多分いらないやつ　多・・・
       // return true;
   //}

    public void execute() {
        if (!this.isEndif) {
            this.parent.isIfFalse = calc(this.conditional) == 0.0D;

        } else {
            this.parent.isIfFalse = false;
        }

    }
}
