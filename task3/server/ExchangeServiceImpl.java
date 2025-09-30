import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;
import java.util.HashMap;
import java.util.Map;

public class ExchangeServiceImpl extends UnicastRemoteObject implements ExchangeService {

    private static final Map<Integer, Map<String, Object>> patients = new HashMap<>();

    static {
        patients.put(1, Map.of("patient_id", 1, "name", "Isha Patil", "age", 25));
        patients.put(2, Map.of("patient_id", 2, "name", "Srishti Yadav", "age", 23));
        patients.put(3, Map.of("patient_id", 3, "name", "Vedanti Ghanekar", "age", 24));
        patients.put(4, Map.of("patient_id", 4, "name", "Shreya Sathish", "age", 22));
        patients.put(5, Map.of("patient_id", 5, "name", "Poorva Kale", "age", 26));
    }

    public ExchangeServiceImpl() throws RemoteException {
        super();
    }

    @Override
    public Map<String, Object> exchangebydoctor(int doctorId, int patientId) throws RemoteException {
        System.out.println("[RMI] Doctor " + doctorId + " requests access to Patient " + patientId);

        if (!patients.containsKey(patientId)) {
            return Map.of("status", "error", "message", "Patient ID Invalid");
        }

        return Map.of("status", "success", "patient_details", patients.get(patientId));
    }
}
