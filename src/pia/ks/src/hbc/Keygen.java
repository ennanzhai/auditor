package hbc;

import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import java.util.Random;

import paillierp.key.KeyGen;
import paillierp.key.PaillierPrivateThresholdKey;

public class Keygen {
	public static void run(int n){
		Random rnd = new Random ();
		PaillierPrivateThresholdKey [] keys =
		KeyGen.PaillierThresholdKey (128 , 2 * n , n , rnd.nextLong () );
		
		int i = 0;
		for (i = 0; i < n; i++){
			try{
				FileOutputStream fs = new FileOutputStream(i + ".key");
				ObjectOutputStream os = new ObjectOutputStream(fs);
				os.writeObject(keys[i]);
				os.close();
			}catch(Exception e){
				e.printStackTrace();
			}
		}		
	}
	
	public static void main(String args[]){
		int n = 3;
		if (args.length > 1){
			n = Integer.parseInt(args[1]);
		}
		run(n);
	}
}
