package mcheli.reHud;
import net.minecraft.util.Vec3;

public class RotationVector {

	Vec3 VEC=Vec3.createVectorHelper(0, 0, 0);


    public Vec3 main(double yaw,double pitch) {
        double[] rotationVector = createRotationVector(yaw, pitch);
        VEC.xCoord=rotationVector[0];
        VEC.yCoord=rotationVector[1];
        VEC.zCoord=rotationVector[2];

        return VEC;

        //MCH_Lib.Log("ARRAY NUM="+rotationVector.length);

       // System.out.println(Arrays.toString(rotationVector));
    }

    public double[] createRotationVector(double yaw, double pitch) {
        // ラジアンへの変換
        double yawRad = Math.toRadians(yaw);
        double pitchRad = Math.toRadians(pitch);

        // 回転行列の作成
        double[][] yawRotation = {
            { Math.cos(yawRad), -Math.sin(yawRad), 0 },
            { Math.sin(yawRad), Math.cos(yawRad), 0 },
            { 0, 0, 1 }
        };

        double[][] pitchRotation = {
            { 1, 0, 0 },
            { 0, Math.cos(pitchRad), -Math.sin(pitchRad) },
            { 0, Math.sin(pitchRad), Math.cos(pitchRad) }
        };

        // 初期ベクトルの作成（Z軸正方向を表す）
        double[] vector = { 0, 0, 1 };

        // ベクトルの回転
        double[] rotatedVector = matrixVectorMultiply(yawRotation, matrixVectorMultiply(pitchRotation, vector));

        return rotatedVector;
    }

    public double[] matrixVectorMultiply(double[][] matrix, double[] vector) {
        int m = matrix.length;
        int n = matrix[0].length;
        int v = vector.length;

        double[] result = new double[m];

        for (int i = 0; i < m; i++) {
            double sum = 0;
            for (int j = 0; j < n; j++) {
                sum += matrix[i][j] * vector[j];
            }
            result[i] = sum;
        }

        return result;
    }
}
