import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class RMIServer {
    public static void main(String[] args) {
        try {
            ExchangeService service = new ExchangeServiceImpl();
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("ExchangeService", service);
            System.out.println("RMI Server is running...");
        } catch (RemoteException e) {
            System.err.println("RMI Server Exception: " + e.toString());
        }
    }
}