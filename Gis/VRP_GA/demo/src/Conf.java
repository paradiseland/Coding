import java.io.*;
import java.util.Scanner;

/**
 * @author minasora
 * @date 2019/10/7 16:16
 * @description 鍌ㄥ瓨闂鐨勫叕鍏辫缃紝椤惧鏁帮紝瀹归噺绾︽潫绛�,杈撳叆杈撳嚭鍑芥暟
 */
public class Conf {
    static int N; // 椤惧鏁�
    static int Cap; // 瀹归噺绾︽潫
    static String instance_name;
    static double[][] dis_matriax;//璺濈鐭╅樀
    static Customer [] customers;//椤惧
    static void readInstance() throws IOException
    {
        File file_to_read = new File("C101.txt");
        Scanner cin = new Scanner(file_to_read);
        instance_name = cin.nextLine();
        N = cin.nextInt();
        Cap = cin.nextInt();
        customers = new Customer[N+1];//鏂板缓鏁扮粍
        dis_matriax = new double[N+1][N+1];
        while(cin.hasNext())
        {
            int i = cin.nextInt();
            customers[i] = new Customer();
            customers[i].x = cin.nextInt();
            customers[i].y = cin.nextInt();
            customers[i].demand = cin.nextInt();
            customers[i].r_time = cin.nextInt();
            customers[i].d_time = cin.nextInt();
            customers[i].s_time = cin.nextInt();
        }
        for(int i=0;i<=N;i++) // 鍒濆鍖栬窛绂荤煩闃�
            for(int j=i;j<=N;j++)
            {
                if(i==j)
                {
                    dis_matriax[i][j] = 0;
                }
                else
                {
                    dis_matriax[i][j] = Customer_Strategy.dis(customers[i],customers[j]);
                    dis_matriax[j][i] = dis_matriax[i][j];
                }
            }


    }
}
