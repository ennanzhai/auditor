package hbc;

import java.io.Serializable;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Random;

public class Polynomial implements Serializable {
	protected ArrayList<BigInteger> coefficients = null;
	protected boolean isEncrypt = false;
	
	/**
	 * get a random polynomial
	 * @param n the degree of polynomial
	 * @return the polynomial
	 */
	public static Polynomial getRandomPolynomial(int n){
		Polynomial p = new Polynomial(n);
		Random rnd = new Random();
		p.coefficients.add(BigInteger.valueOf(rnd.nextLong()));
		return p;
	}
	 
	public Polynomial(int n){
		coefficients = new ArrayList<BigInteger>(n);
	}
	
	
	/**
	 * get the (index)th of coefficients
	 * @param index 
	 * @return
	 */
	public BigInteger get(int index){
		if (coefficients == null){
			System.err.println("invalid polynomial");
		}
		
		return coefficients.get(index);
	}
	
	/**
	 * get inputSet = {x0,x1,..xn}
	 * cal it and produce f = (x-x0)(x-x1)...(x-xn)
	 * =y0+y1x+y2x^2+...ynx^n
	 * coefficients = {y0,y1,..,yn}
	 * @param inputSet
	 */
	public Polynomial(ArrayList<BigInteger> inputSet){
		coefficients = new ArrayList<BigInteger>();
		int i = 0;
		for(i = 0; i < inputSet.size() + 1; i++){
			coefficients.add(new BigInteger("1"));
		}
		
		coefficients.set(0, inputSet.get(0).negate());
		
		int j = 0;
		for (i = 1; i < inputSet.size(); i++){
			for (j = i; j > 0; j--){
				coefficients.set(j, coefficients.get(j - 1).subtract(coefficients.get(j).multiply(inputSet.get(i))));
			}
			coefficients.set(0, coefficients.get(0).multiply(inputSet.get(i).negate()));
		}
		
		for(i = 0; i < coefficients.size(); i++){
			coefficients.set(i, coefficients.get(i).mod(BigInteger.valueOf(65535)));
			System.out.println(coefficients.get(i));
		}
	}
	
	public static void main(String[] args){
		System.out.println(BigInteger.valueOf(-1).mod(BigInteger.valueOf(65535)));
		
		
		ArrayList<BigInteger> inputSet1 = new ArrayList<BigInteger>();
		inputSet1.add(new BigInteger("3"));
		inputSet1.add(new BigInteger("2"));

		Polynomial r1 = Polynomial.getRandomPolynomial(2);
		Polynomial r2 = Polynomial.getRandomPolynomial(2);		
		
		ArrayList<BigInteger> inputSet2 = new ArrayList<BigInteger>();
		inputSet2.add(new BigInteger("2"));
		inputSet2.add(new BigInteger("3"));
		inputSet2.add(new BigInteger("15"));
				
		Polynomial p1 = new Polynomial(inputSet1);
		Polynomial p2 = new Polynomial(inputSet2);
		
		PaillierPolynomial paillier = new PaillierPolynomial("0.key");
		Polynomial e1 = paillier.encrypt(p1);
		Polynomial e2 = paillier.encrypt(p2);
		Polynomial e3 = paillier.add(e1, e2);
		
		//e3 = paillier.add(e3, paillier.multiply(e1, p1));
		//e3 = paillier.add( paillier.multiply(e1, r1), paillier.multiply(e2, r2));
		Polynomial d3 = paillier.decryptOnly(e3);
		
		System.out.println(d3.coefficients.toString());
		
		BigInteger v = paillier.getValue(e3, BigInteger.valueOf(3));
		BigInteger d4 = paillier.decryptOnly(v);
		System.out.println(d4.mod(BigInteger.valueOf(65535)));
	}
}
