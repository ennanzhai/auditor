package hbc;

import java.io.FileInputStream;
import java.io.ObjectInputStream;
import java.util.ArrayList;

import java.math.BigInteger;

import paillierp.PaillierThreshold;
import paillierp.PartialDecryption;
import paillierp.key.PaillierPrivateThresholdKey;
import paillierp.zkp.DecryptionZKP;

public class PaillierPolynomial {
	public static BigInteger scope = BigInteger.valueOf(65535);
	private PaillierThreshold paillier = null;
	
	/**
	 * get paillier key form a file
	 * @param filename the file contains key
	 */
	public PaillierPolynomial(String fileName){
		try{			
            FileInputStream fis = new FileInputStream(fileName);
            ObjectInputStream ois = new ObjectInputStream(fis);
            PaillierPrivateThresholdKey key = (PaillierPrivateThresholdKey) ois.readObject();
            paillier = new PaillierThreshold(key);
            ois.close();
		}catch(Exception e){
			e.printStackTrace();
		}			
	}
	
	/**
	 * encrypt a Polynomial p
	 * @return encrypt(p)
	 */
	public Polynomial encrypt(Polynomial p){
		if (paillier == null){
			System.err.println("You must get paillier before encrypt");
			return null;
		}
		
		Polynomial res = new Polynomial(p.coefficients.size());
		int i = 0;
		for(i = 0; i < p.coefficients.size(); i++){
			BigInteger num = p.coefficients.get(i);
			if (num.compareTo(BigInteger.valueOf(0)) >= 0){
				res.coefficients.add(paillier.encrypt(num));
			}else{
				// there are some problem in pailier.jar in negative BigInteger
				// I make it work by encrypt(-num), then multiply it with -1
				BigInteger positiveNum = num.negate();
				BigInteger encrypyPositiveNum = paillier.encrypt(positiveNum);
				res.coefficients.add(  paillier.multiply(encrypyPositiveNum, -1));
			}
			
		}
		res.isEncrypt = true;

		return res;
	}
	
	/**
	 * cal encrypt(this + other)
	 * @param other
	 * @return encrypt(this + other)
	 */
	public Polynomial add(Polynomial p1, Polynomial p2){
		if (p1 == null || p2 == null){
			System.err.println("Please input an encrypt polynmial");
			return null;
		}
		
		int p1Size = p1.coefficients.size();
		int p2Size = p2.coefficients.size();
		int max = p1Size;
		if (p2Size > max){
			max = p2Size;
		}
		
		Polynomial res = new Polynomial(max);
		int i = 0;
		for (i = 0; i < max; i++){
			if (i >= p1Size){
				res.coefficients.add(p2.coefficients.get(i));
			}else if(i >= p2Size){
				res.coefficients.add(p1.coefficients.get(i));
			}else{
				res.coefficients.add( paillier.add(p1.coefficients.get(i), p2.coefficients.get(i)) );
			}
		}
		res.isEncrypt = true;
		return res;
	}
	
	/**
	 * multiply an encrypt poly with an unencrypt poly
	 * @param p1 encrypt poly
	 * @param p2 unencrypy poly
	 * @return
	 */
	public Polynomial multiply(Polynomial p1, Polynomial p2){
		if (p1 == null || p2 == null){
			System.err.println("Please input an encrypt polynmial");
			return null;
		}
		
		int p1Size = p1.coefficients.size();
		int p2Size = p2.coefficients.size();
		int max = p1Size + p2Size - 1;
		
		Polynomial res = new Polynomial(max);
		int i = 0, j = 0;
		for (i = 0; i < max; i++){
			res.coefficients.add( paillier.encrypt(BigInteger.valueOf(0)));
			for (j = 0; j < p1Size; j++){
				if (i - j < 0 || i - j > p2Size - 1){
					continue;
				}
				// p2 is const
				BigInteger mul = paillier.multiply(p1.coefficients.get(j), p2.coefficients.get(i - j).mod(scope));
				res.coefficients.set(i, paillier.add(res.coefficients.get(i), mul));
			}
		}
		
		return res;
	}
	
	/**
	 * get the value of polynomial at a unencrypt point
	 * @param p the polynomial
	 * @param c the point
	 * @return encrypt of p(i)
	 */
	public BigInteger getValue(Polynomial p, BigInteger c){
		BigInteger res = paillier.encrypt(BigInteger.valueOf(0));
		BigInteger mul = BigInteger.valueOf(1);
		
		int i = 0;
		for (i = 0; i < p.coefficients.size(); i++){
			res = paillier.add(res, paillier.multiply(p.coefficients.get(i), mul));
			mul = mul.multiply(c).mod(scope);
		}
		return res;
	}

	/**
	 * decrypt a ArrayList of BigInteger into zkp
	 * @param arr the ArrayList to decrypt
	 * @return the zkp array
	 */
	public ArrayList<DecryptionZKP> decryptProof(ArrayList<BigInteger> arr){
		ArrayList<DecryptionZKP> res = new ArrayList<DecryptionZKP>();
		
		int i = 0;
		for (i = 0; i < arr.size(); i++){
			res.add(paillier.decryptProof( arr.get(i)));
		}
		return res;
	}	

	public BigInteger combineShares(DecryptionZKP arr[]){	
		return paillier.combineShares(arr);
	}	
	
	public BigInteger combineShares(ArrayList<PartialDecryption> arg){
		PartialDecryption arr[] = new PartialDecryption[arg.size()];
		for (int i = 0; i < arg.size(); i++){
			arr[i] = arg.get(i);
		}
		return paillier.combineShares(arr).mod(scope);
	}

	
	public ArrayList<PartialDecryption> decrypt(ArrayList<BigInteger> arr){
		ArrayList<PartialDecryption> res = new ArrayList<PartialDecryption>();
		
		int i = 0;
		for (i = 0; i < arr.size(); i++){
			res.add(paillier.decrypt( arr.get(i)));
		}
		return res;
	}
	
	/**
	 * decrypt zero-knowledge
	 * @param p the polynomial want to decrypt
	 * @return the zkp array
	 */
	public ArrayList<DecryptionZKP> decryptProof(Polynomial p){
		ArrayList<DecryptionZKP> res = new ArrayList<DecryptionZKP>();
		
		int i = 0;
		for (i = 0; i < p.coefficients.size(); i++){
			res.add(paillier.decryptProof( p.coefficients.get(i)));
		}
		return res;
	}
	
	/**
	 * decrypt a polynomial only by itself
	 * @param p the polynomial want to decrypt
	 * @return the decrypt of the polynomial
	 */
	public Polynomial decryptOnly(Polynomial p){
		Polynomial res = new Polynomial(p.coefficients.size());
		int i = 0;
		for (i = 0; i < p.coefficients.size(); i++){
			DecryptionZKP s = paillier.decryptProof(p.coefficients.get(i));
			res.coefficients.add( paillier.combineShares(s));
		}
		
		return res;
	}

	public BigInteger decryptOnly(BigInteger bi){
		
		DecryptionZKP s = paillier.decryptProof(bi);
		return paillier.combineShares(s).mod(scope);
	}
	
}
