import { useState, useEffect } from 'react';
import { useFetchEmployeesQuery, useFetchAvailabilityQuery, useAddPrenotationMutation } from '@/redux/features/centerApiSLice';
import { useParams } from 'next/navigation';

const PrenotationForm = () => {
  const [type, setType] = useState<string>('nutritionist');
  const [date, setDate] = useState<string>('');
  const [duration, setDuration] = useState<number>(0.5); // Default to 0.5 for nutritionist
  const [selectedSlot, setSelectedSlot] = useState<string>(''); // New state to track selected slot
  const { uuid } = useParams();
  const centerUuid = Array.isArray(uuid) ? uuid[0] : uuid;
  const [employeeUuid, setEmployeeUuid] = useState<string | null>(null);
  const [selectEmployee, setSelectEmployee] = useState<boolean>(false);

  // Fetch employees based on centerUuid
  const { data: employeesData } = useFetchEmployeesQuery({ center_uuid: centerUuid });

  // Fetch availability slots
  const { data: availableSlotsData, refetch } = useFetchAvailabilityQuery(
    {
      type, 
      date, 
      duration, 
      centerUuid: centerUuid, 
      employeeUuid: selectEmployee && employeeUuid ? employeeUuid : undefined
    }, 
    {
      skip: !date || !centerUuid, // Skip fetch until all necessary data is present
    }
  );

  // Mutation for adding a new prenotation
  const [addPrenotation, { isLoading, isError, isSuccess }] = useAddPrenotationMutation();

  // Effettua la chiamata API quando l'utente esce dal campo data
  const handleDateBlur = () => {
    if (date && type && centerUuid) {
      refetch(); // Refetch availability slots
    }
  };

  // Aggiorna la durata quando il tipo di sessione cambia
  useEffect(() => {
    if (type === 'nutritionist') {
      setDuration(0.5); // Set duration to 0.5 if type is nutritionist
    } else if (type === 'trainer') {
      setDuration(1); // Default for trainer (adjust as needed)
    }
  }, [type]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Extract from_hour and to_hour from selectedSlot
    const [fromHour, toHour] = selectedSlot.split(' - ');

    // Combine date and time, ensuring correct formatting
    const from_hour = new Date(`${date}T${fromHour}`).toISOString();
    const to_hour = new Date(`${date}T${toHour}`).toISOString();

    const prenotationData = {
      type,
      from_hour,
      to_hour,
      center_uuid: centerUuid,
      employee_uuid: selectEmployee && employeeUuid ? employeeUuid : undefined,
    };

    try {
      await addPrenotation(prenotationData).unwrap();
      // Handle success, e.g., show a success message or redirect
      console.log('Prenotazione aggiunta con successo');
    } catch (error) {
      // Handle error, e.g., show an error message
      console.error('Errore durante l\'aggiunta della prenotazione:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-6 text-center">Prenota una Sessione</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-5">
          <label htmlFor="type" className="block text-gray-700 text-lg font-medium">Tipo di Sessione</label>
          <select
            id="type"
            value={type}
            onChange={(e) => setType(e.target.value)}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="nutritionist">Nutritionist</option>
            <option value="trainer">Trainer</option>
          </select>
        </div>

        <div className="mb-5">
          <label htmlFor="date" className="block text-gray-700 text-lg font-medium">Data</label>
          <input
            type="date"
            id="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            onBlur={handleDateBlur} // Trigger API call when the input loses focus
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div className="mb-5">
          <label htmlFor="duration" className="block text-gray-700 text-lg font-medium">Durata (ore)</label>
          <input
            type="number"
            id="duration"
            value={duration}
            step={0.1} // Allows decimal values
            onChange={(e) => setDuration(parseFloat(e.target.value))}
            min={0.5}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
            readOnly={type === 'nutritionist'} // Readonly if type is nutritionist
          />
        </div>

        <div className="mb-5">
          <label className="block text-gray-700 text-lg font-medium">Vuoi selezionare un dipendente specifico?</label>
          <input
            type="checkbox"
            checked={selectEmployee}
            onChange={(e) => setSelectEmployee(e.target.checked)}
            className="mt-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {selectEmployee && (
          <div className="mb-5">
            <label htmlFor="employee" className="block text-gray-700 text-lg font-medium">Dipendente</label>
            <select
              id="employee"
              value={employeeUuid || ''}
              onChange={(e) => setEmployeeUuid(e.target.value)}
              className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Seleziona un dipendente</option>
              {employeesData?.employees.map((employee) => (
                <option key={employee.uuid} value={employee.uuid}>
                  {employee.first_name} {employee.last_name}
                </option>
              ))}
            </select>
          </div>
        )}

        <div className="mb-5">
          <label htmlFor="availableSlots" className="block text-gray-700 text-lg font-medium">Slot Disponibili</label>
          <select
            id="availableSlots"
            value={selectedSlot} // Track the selected slot
            onChange={(e) => setSelectedSlot(e.target.value)} // Update the selected slot
            required
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Seleziona uno slot</option>
            {availableSlotsData?.availability.map((slot, index) => (
              <option key={index} value={`${slot[0]} - ${slot[1]}`}>
                {slot[0]} - {slot[1]}
              </option>
            ))}
          </select>
        </div>

        <button
          type="submit"
          className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isLoading} // Disable button if mutation is in progress
        >
          {isLoading ? 'Prenotazione in corso...' : 'Prenota'}
        </button>

        {isSuccess && <p className="text-green-500 mt-4">Prenotazione avvenuta con successo!</p>}
        {isError && <p className="text-red-500 mt-4">Si è verificato un errore durante la prenotazione.</p>}
      </form>
    </div>
  );
};

export default PrenotationForm;
