import java.io.Serializable;
import java.math.BigInteger;
import java.util.ArrayList;


public class Msg implements Serializable{
	
	public String type = "TypeNone";
	public String origin = "";
	public ArrayList<String> encryptedBy = null;
	public ArrayList<String> whoGot = null;
	public ArrayList<BigInteger> content = null;
	public BigInteger pubKey = null;
	public BigInteger bigB_n = null;
	
	public Msg(){
		type = "TypeNone";
		origin = "";
		encryptedBy = null;
		whoGot = null;
		content = null;
		pubKey = null;
		bigB_n = null;
	}
	
	public Msg(String t,String or, ArrayList<String> by, ArrayList<BigInteger> con ){
		type = t;
		origin = or;
		encryptedBy = by;
		content = con;
		whoGot = new ArrayList<String>();
		pubKey = null;
		bigB_n = null;
	}
	
	public static Msg createMyNewFileMsg(){
		String t_tmp = "PassOnToEncrypt";
		ArrayList<String> by_tmp = new ArrayList<String>();
		by_tmp.add(TCPsocket.nodeName);
		ArrayList<BigInteger> con_tmp = TCPsocket.myData.encryptedMyFile;
		return new Msg(t_tmp,TCPsocket.nodeName, by_tmp, con_tmp );
	}
	
	
	public static Msg createMyPubKeyMsg(BigInteger pub){
		Msg msg = new Msg();
		msg.type = "MyPubKey";
		msg.pubKey = pub;
		return msg;
	}
	
	public static Msg createBigNMsg(BigInteger bign, BigInteger pub){
		Msg msg = new Msg();
		msg.type = "BigN";
		msg.bigB_n = bign;
		msg.pubKey = pub;
		return msg;
		
	}
}
