// components/ExitForm.tsx

import React, { useState } from 'react';
import { useAddExitMutation } from '@/redux/features/centerApiSLice';
import { useParams } from 'next/navigation';

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toISOString().split('T')[0]; // Formatta la data in YYYY-MM-DD
};

const ExitForm: React.FC = () => {
  const { uuid } = useParams();
  const types = [
    'salary', 'single', 'tax',
  ];


  const [formData, setFormData] = useState({
    amount: '',
    type: '',
    employee_uuid: '',
    frequency: '',
    description: '',
    start_date: '',
    expiration_date: '',
  });

  const [addExit, { isLoading, isSuccess, isError, error }] = useAddExitMutation();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await addExit({
        amount: Number(formData.amount),
        type: formData.type,
        employee_uuid: formData.employee_uuid,
        frequency: Number(formData.frequency),
        description: formData.description,
        start_date:formatDate(formData.start_date),
        expiration_date: formatDate(formData.expiration_date),
        center_uuid: uuid as string,
      }).unwrap();
      // Reset form or handle success as needed
      setFormData({
        amount: '',
        type: '',
        employee_uuid: '',
        frequency: '',
        description: '',
        start_date: '',
        expiration_date: '',
      });
    } catch (err) {
      console.error('Failed to save exit: ', err);
    }
  };

  return (
    <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-6 text-center">Aggiungi Exit</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-5">
          <label htmlFor="amount" className="block text-gray-700 text-lg font-medium">Amount</label>
          <input
            type="number"
            id="amount"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-5">
          <label htmlFor="type" className="block text-gray-700 text-lg font-medium">Type</label>
          <select
            id="type"
            name="type"
            value={formData.type}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="">Select type</option>
            {types.map(prov => (
              <option key={prov} value={prov}>{prov}</option>
            ))}
          </select>
        </div>
        <div className="mb-5">
          <label htmlFor="employee_uuid" className="block text-gray-700 text-lg font-medium">Employee UUID</label>
          <input
            type="text"
            id="employee_uuid"
            name="employee_uuid"
            value={formData.employee_uuid}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-5">
          <label htmlFor="frequency" className="block text-gray-700 text-lg font-medium">Frequency</label>
          <input
            type="number"
            id="frequency"
            name="frequency"
            value={formData.frequency}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-5">
          <label htmlFor="description" className="block text-gray-700 text-lg font-medium">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={4}
            required
          />
        </div>
        <div className="mb-5">
          <label htmlFor="start_date" className="block text-gray-700 text-lg font-medium">Start Date</label>
          <input
            type="date"
            id="start_date"
            name="start_date"
            value={formData.start_date}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-5">
          <label htmlFor="expiration_date" className="block text-gray-700 text-lg font-medium">Expiration Date</label>
          <input
            type="date"
            id="expiration_date"
            name="expiration_date"
            value={formData.expiration_date}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            
          />
        </div>
        <button
          type="submit"
          className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Submit
        </button>
        {isSuccess && <p className="text-green-500 mt-4">Exit added successfully!</p>}
      </form>
    </div>
  );
};

export default ExitForm;
