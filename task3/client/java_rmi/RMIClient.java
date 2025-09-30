import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Map;
import java.util.Scanner;

public class RMIClient {
    public static void main(String[] args) {
        try {
            Registry registry = LocateRegistry.getRegistry("172.16.233.206", 1099);
            ExchangeService stub = (ExchangeService) registry.lookup("ExchangeService");

            Scanner sc = new Scanner(System.in);
            System.out.print("Enter your Doctor ID: ");
            int doctorId = sc.nextInt();
            System.out.print("Enter Patient ID to access: ");
            int patientId = sc.nextInt();

            Map<String, Object> response = stub.exchangebydoctor(doctorId, patientId);
            System.out.println("Response from server: " + response);
            sc.close();
        } catch (NotBoundException | RemoteException e) {
            System.err.println("RMI Client Exception: " + e.toString());
        }
    }
}
