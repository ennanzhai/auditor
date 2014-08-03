package hbc;

import java.net.*; 
import java.util.ArrayList;
import java.io.*; 

public class Server {
	private int colludingNum = 1; 
	private int playerNum = 2;
	
	public static int PORT = 9531;
	/**
	 * @param c 
	 * dishonest colluding 
	 * @param n
	 * the number of client
	 */
	public Server(int c, int n){
		this.colludingNum = c;
		this.playerNum = n;
	}

		
	/**
	 * run server to collect all player's ip,
	 * and send colludingNum and playerNum to them
	 */
	public void run(){
		try{
			ServerSocket serverSocket = new ServerSocket(PORT,playerNum,InetAddress.getLocalHost());
			System.out.println("listening in addr:" + serverSocket.getLocalSocketAddress());
			ArrayList<Socket> peerSocketList = new ArrayList<Socket>();
			
			// each player will send his listening ip/port to server,
			// then server will broadcast to everyone
			ArrayList<SocketAddress> playerAddrList = new ArrayList<SocketAddress>();
			int i = 0;
			for (i = 0; i < playerNum; i++){
				System.out.println("waiting for connection");
				Socket peerSocket = serverSocket.accept();				
				System.out.println("Client" + i + "connected");
				
				peerSocketList.add(peerSocket);
				ObjectOutputStream out = new ObjectOutputStream(peerSocket.getOutputStream());
				out.writeObject(i);
				out.writeObject(colludingNum);
				out.writeObject(playerNum);
				
				ObjectInputStream in = new ObjectInputStream(peerSocket.getInputStream());
				SocketAddress addr = (SocketAddress)in.readObject();
				playerAddrList.add(addr);
				
				// close out or in will close socket..
				//out.close();
				//in.close();
			}
			
			for (i = 0; i < playerNum; i++){
				System.out.println(playerAddrList.get(i));
				ObjectOutputStream out = new ObjectOutputStream(peerSocketList.get(i).getOutputStream());
				out.writeObject(playerAddrList);
				peerSocketList.get(i).close();
			}
			
			serverSocket.close();
		}catch (Exception e){
			e.printStackTrace();
		}
	}
	
	public void run2(){
		try{
			//ServerSocket serverSocket = new ServerSocket(PORT,playerNum,InetAddress.getLocalHost());
			ServerSocket serverSocket = new ServerSocket(PORT,playerNum,InetAddress.getLocalHost());
			Socket peerSocket = serverSocket.accept();
			peerSocket.close();
			serverSocket.close();
		}catch (Exception e){
			e.printStackTrace();
		}		
	}
	
	public static void main(String args[]){
		Server server = new Server(1,2);
		server.run();
	}
}
