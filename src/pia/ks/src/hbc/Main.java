package hbc;

import paillierp.Paillier;
import paillierp.PaillierThreshold;
import paillierp.PartialDecryption;

import java.io.*;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Random;

import paillierp.key.KeyGen;
import paillierp.key.PaillierPrivateThresholdKey;
import paillierp.zkp.DecryptionZKP;


public class Main {
	public static void main(String[] args){
		System.out.println (" Create new keypairs .");
		Random rnd = new Random ();
		PaillierPrivateThresholdKey [] keys =
		KeyGen.PaillierThresholdKey (128 , 6 , 2 , rnd.nextLong () );
		System.out.println (" Six keys are generated , with a threshold of 3.");
		System.out.println (" Six people use their keys : p1 , p2 , p3 , p4 , p5 , p6 ");

		
		try{
			FileOutputStream fs = new FileOutputStream("key");
			ObjectOutputStream os = new ObjectOutputStream(fs);
			os.writeObject(keys[0]);
			os.close();
			
            FileInputStream fis = new FileInputStream("key");
            ObjectInputStream ois = new ObjectInputStream(fis);
            keys[0] = (PaillierPrivateThresholdKey) ois.readObject();
            ois.close();
		}catch(Exception e){
			e.printStackTrace();
		}
		System.out.println(keys[0].getPublicKey().toString());
		
		PaillierThreshold p1 = new PaillierThreshold(keys [0]);
		PaillierThreshold p2 = new PaillierThreshold(keys [1]);
		PaillierThreshold p3 = new PaillierThreshold(keys [2]);
		PaillierThreshold p4 = new PaillierThreshold(keys [3]);
		PaillierThreshold p5 = new PaillierThreshold(keys [4]);
		PaillierThreshold p6 = new PaillierThreshold(keys [5]);
		
		BigInteger m1 = new BigInteger("1");
		BigInteger m2 = new BigInteger("4");
		BigInteger e1 = p1.encrypt(m1);
		BigInteger e2 = p2.encrypt(m2);
		BigInteger e3 = p1.add(p1.multiply(e2, -1), e1);
		e3 = p1.add(e3, e2);
		
		DecryptionZKP s1 = p1.decryptProof(e3);
		//BigInteger dec2 = p1.combineShares(s1);
		//System.out.println("dec2 = " + dec2);
		
		DecryptionZKP s2 = p2.decryptProof(e3);
		DecryptionZKP s3 = p3.decryptProof(e3);		
		BigInteger dec = p1.combineShares(s1 , s2 , s3 );
		
		System.out.println("sum = " + dec);
		
		System.out.println (" Alice is given the public key .");
		Paillier alice = new Paillier(keys [0]. getPublicKey () );
		// Alice encrypts a message
		//BigInteger msg = BigInteger.valueOf (135819283);
		//BigInteger msg1 = BigInteger.valueOf(2);
		BigInteger msg = new BigInteger("1");
		BigInteger msg1 = new BigInteger("4");
		BigInteger Emsg = alice.encrypt(msg );
		BigInteger Emsg1 = alice.encrypt(msg1);
		Emsg1 = p1.multiply(Emsg1, BigInteger.valueOf(-1));
		BigInteger Emsg3 = alice.add(Emsg, Emsg1);
		Emsg = alice.add(Emsg, Emsg1);
		//Emsg = alice.multiply(Emsg, msg1);
		System.out.println (" Alice encrypts the message "+ msg +" and sends "+
		Emsg +" to everyone .");
		// Alice sends Emsg to everyone
		System.out.println (" p1 receives the message and tries to decrypt all alone :");
		BigInteger p1decrypt = p1.decryptOnly(Emsg );
		
		if(p1decrypt.equals(msg ) ) {
		System.out.println (" p1 succeeds decrypting the message all alone .");
		} else {
		System.out.println (" p1 fails decrypting the message all alone.:(");
		}
		System.out.println (" p2 and p3 receive the message and " +
		" create a partial decryptions .");
		DecryptionZKP p2share = p2.decryptProof(Emsg );
		DecryptionZKP p3share = p3.decryptProof(Emsg );
		// p2 sends the partial decryption to p3
		// p3 sends the partial decryption to p2
		System.out.println (" p2 receives the partial p3 ' s partial decryption " +
		" and attempts to decrypt the whole message using its own " +
		" share twice ");
		try {
		BigInteger p2decrypt = p2.combineShares(p2share , p3share , p2share );
		if(p2decrypt.equals(msg ) ) {
		System.out.println (" p2 succeeds decrypting the message with p3 .");
		} else {
		System.out.println (" p2 fails decrypting the message with p3.:(");
		}
		} catch(IllegalArgumentException e ) {
		System.out.println (" p2 fails decrypting and throws an error ");
		}
		System.out.println (" p4 , p5 , p6 receive Alice ' s original message and " +
		" create partial decryptions .");
		DecryptionZKP p4share = p4.decryptProof(Emsg );
		DecryptionZKP p5share = p5.decryptProof(Emsg );
		DecryptionZKP p6share = p6.decryptProof(Emsg );
		// p4 , p5 , and p6 share each of their partial decryptions with each other
		System.out.println (" p4 receives and combines each partial decryption " + " to decrypt whole message :");
		BigInteger p4decrypt = p4.combineShares(p4share , p5share , p6share );
		if(p4decrypt.equals(msg)) {
			System.out.println (" p4 succeeds decrypting the message with p5 and p6.");
		} else {
			System.out.println (" p4 fails decrypting the message with p5 and p6 .");
		}
		System.out.println(p4decrypt);
		
		
		PartialDecryption par1 = p1.decrypt(e3);
		PartialDecryption par2 = p2.decrypt(e3);
		BigInteger ans = p1.combineShares(par1, par2);
		System.out.println(ans);
		//ArrayList<DecryptionZKP> comlist = new ArrayList<DecryptionZKP>();
		//comlist.add(p2share);
		//BigInteger decrpttest = p2.combineShares(comlist.toArray());
		//DecryptionZKP[] c = (DecryptionZKP [])comlist.toArray();
		//p2.combineShares(c);
	}
}
