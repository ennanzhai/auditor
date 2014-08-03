import java.math.BigInteger;
import java.util.Random;


public class PohligHellman {

	private static BigInteger bigB_P_1_Q_1 = BigInteger.ZERO;
	public static BigInteger bigB_N = BigInteger.ZERO;
	//------server use--------------------------
	public static BigInteger generateKey(){
		//key generation:
		Random rand1 = new Random(System.currentTimeMillis());   // Generating a random number/
		Random rand2 = new Random(System.currentTimeMillis()*10);  // Generating another random number
		// code for receiving public keys from all the parties (e.g., Alice, Bob, etc. ) 
		BigInteger bigB_p = BigInteger.probablePrime(512, rand1);   // 512 is a default size
		BigInteger bigB_q = BigInteger.probablePrime(512, rand2);
		BigInteger bigB_n = bigB_p.multiply(bigB_q);
		BigInteger bigB_p_1 = bigB_p.subtract(BigInteger.ONE);  //p-1
		BigInteger bigB_q_1 = bigB_q.subtract(BigInteger.ONE);  //q-1
		BigInteger bigB_p_1_q_1 = bigB_p_1.multiply(bigB_q_1);
		PohligHellman.bigB_P_1_Q_1 = bigB_p_1_q_1;
		PohligHellman.bigB_N = bigB_n;
		return bigB_n;
	}
	
	public static BigInteger revisePubKey (BigInteger pubKey_Alice){
		// we want gcd ==1 
		BigInteger BigB_GCD = PohligHellman.bigB_P_1_Q_1.gcd(pubKey_Alice);
	    while (!BigB_GCD.equals(BigInteger.ONE)){
	        pubKey_Alice = pubKey_Alice.add(BigInteger.ONE);
	        BigB_GCD = PohligHellman.bigB_P_1_Q_1.gcd(pubKey_Alice);
	    }
		return pubKey_Alice;
	}
	
	
	//------client use----------------
	public static BigInteger generatePubKey(){
		Random ran = new Random(System.currentTimeMillis());
		BigInteger pub =  BigInteger.valueOf( ran.nextInt(99999));
		return pub;
	}
	
	public static BigInteger encrypt (BigInteger val, BigInteger pubKey, BigInteger bigB_n){
		BigInteger bigB_cipherVal = val.modPow(pubKey, bigB_n);  
		return bigB_cipherVal;
	}
	
	
	
}