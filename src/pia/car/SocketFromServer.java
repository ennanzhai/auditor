import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.math.BigInteger;
import java.net.Socket;
import java.net.UnknownHostException;


public class SocketFromServer extends Thread {

	public String ip = "";
	public int port = 0;
	public Socket nodeSocket = null;
    public ObjectOutputStream outputStream = null;
    public ObjectInputStream inputStream = null;
    
    public BigInteger pub_origin = BigInteger.ZERO;
    public BigInteger pub_final = BigInteger.ZERO;
    
	
	public SocketFromServer(String ip, int port){
		this.ip = ip;
		this.port = port;
		start();
		
	}
	public void run(){
		try {
            nodeSocket = new Socket(ip, port);
            outputStream = new ObjectOutputStream(nodeSocket.getOutputStream());
			inputStream = new ObjectInputStream(nodeSocket.getInputStream());
			
        } catch (UnknownHostException e) {
            System.err.println("Don't know about host: " + ip);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Couldn't get I/O for "
                               + "the connection to: " + ip);
            System.exit(1);
        }
        System.out.println("[Server node] connected to "+this.ip + ":" + this.port);
        
        waitingForNodeMsgObj();
	}
	
	public void waitingForNodeMsgObj(){
		Msg msgIn = null;
		try {
			msgIn = (Msg) inputStream.readObject();
			pendingMsgObjFromNodes(msgIn);
			
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	

	private void pendingMsgObjFromNodes(Msg msgObj){
		// check message
		System.out.println("[From Node]" + msgObj.type );
		if (msgObj.type.equals("MyPubKey")){
			// store into server node 
			this.pub_origin = msgObj.pubKey;
		}
	}

	public void sendObjToNodes(Msg obj){
			try {
				outputStream.writeObject(obj);
				outputStream.flush();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		
	}
	
}

