import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.rmi.registry.LocateRegistry; 
import java.rmi.registry.Registry;
import java.util.Scanner;

public class Client { 
  private Client() {} 

  public static void main(String[] args) { 
    String host = (args.length < 1) ? null : args[0];
    String opc;
    long startTime;
    File clientPathFile;
    byte [] myData;
    FileInputStream in;
    long endTime;
    long totalTime;

    // Menu
    Scanner userInput = new Scanner(System.in);
    System.out.println("Escolha o tamanho do arquivo a ser enviado: ");    
    System.out.println("1 - 1 Mb");
    System.out.println("2 - 5 Mb");
    System.out.println("3 - 100 Mb");
    System.out.println("4 - 1 Gb"); 
    opc = userInput.nextLine();
    try {
      Registry registry = LocateRegistry.getRegistry(host); 
      UploadFile uplaod = (UploadFile) registry.lookup("UploadFile"); 
      switch (opc) {
        case "1":
          startTime = System.nanoTime();
          
          clientPathFile = new File("1Mb.txt");
          myData = new byte[(int) clientPathFile.length()];
          in = new FileInputStream(clientPathFile);	
          in.read(myData, 0, myData.length);
          uplaod.uploadFile("1Mb", myData);          
          in.close();

          endTime   = System.nanoTime();
          totalTime = endTime - startTime;
          System.out.println(totalTime + " nano seg");
          System.out.println(totalTime/1000000000 + " seg");
        break;
        case "2":
          startTime = System.nanoTime();
          
          clientPathFile = new File("5Mb.txt");
          myData = new byte[(int) clientPathFile.length()];
          in = new FileInputStream(clientPathFile);	
          in.read(myData, 0, myData.length);
          uplaod.uploadFile("5Mb", myData);          
          in.close();

          endTime   = System.nanoTime();
          totalTime = endTime - startTime;
          System.out.println(totalTime + " nano seg");
          System.out.println(totalTime/1000000000 + " seg");        break;
        case "3":
          startTime = System.nanoTime();
          
          clientPathFile = new File("100Mb.txt");
          myData = new byte[(int) clientPathFile.length()];
          in = new FileInputStream(clientPathFile);	
          in.read(myData, 0, myData.length);
          uplaod.uploadFile("100Mb", myData);          
          in.close();

          endTime   = System.nanoTime();
          totalTime = endTime - startTime;
          System.out.println(totalTime + " nano seg");
          System.out.println(totalTime/1000000000 + " seg");        break;
        case "4":
          startTime = System.nanoTime();
          
          clientPathFile = new File("1Gb.txt");
          myData = new byte[(int) clientPathFile.length()];
          in = new FileInputStream(clientPathFile);	
          in.read(myData, 0, myData.length);
          uplaod.uploadFile("1Gb", myData);          
          in.close();

          endTime   = System.nanoTime();
          totalTime = endTime - startTime;
          System.out.println(totalTime + " nano seg");
          System.out.println(totalTime/1000000000 + " seg");        break;
      }
    } catch (Exception e) { 
		  System.err.println("Client exception: " + e.toString()); 	e.printStackTrace(); 
    } 
  }
} 