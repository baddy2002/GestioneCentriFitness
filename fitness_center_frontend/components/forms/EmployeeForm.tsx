// components/EmployeeForm.tsx

import React, { useState } from 'react';
import { useAddEmployeeMutation } from '@/redux/features/centerApiSLice';
import { useParams } from 'next/navigation';

const formatDate = (dateString: string): string | null => {
  if (dateString != null && dateString != ""){

    const date = new Date(dateString);
    return date.toISOString().split('T')[0]; 
  }
  return null
};

const EmployeeForm: React.FC = () => {
  const { uuid } = useParams();
  
  const types = [
    'nutritionist', 'trainer', 'mixed',
  ];

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    DOB: '',
    salary: '',
    fiscalCode: '',
    email: '',
    type: '',
    hiring_date: '',
    end_contract_date: '',
    attachments_uuid: ''
  });

  const [addEmployee, { isLoading, isSuccess, isError, error }] = useAddEmployeeMutation();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await addEmployee({
        first_name: formData.first_name,
        last_name: formData.last_name,
        DOB: formatDate(formData.DOB)+"",
        salary: Number(formData.salary),
        fiscalCode: formData.fiscalCode,
        email: formData.email,
        type: formData.type,
        hiring_date: formatDate(formData.hiring_date)+"",
        end_contract_date: formData.end_contract_date ? formatDate(formData.end_contract_date) : null,
        attachments_uuid: formData.attachments_uuid ? formData.attachments_uuid : null,
        center_uuid: uuid as string 
      }).unwrap();
      // Reset form or handle success as needed
      setFormData({
        first_name: '',
        last_name: '',
        DOB: '',
        salary: '',
        fiscalCode: '',
        email: '',
        type: '',
        hiring_date: '',
        end_contract_date: '',
        attachments_uuid: ''
      });
    } catch (err) {
      console.error('Failed to save employee: ', err);
    }
  };

  return (
    <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-6 text-center">Aggiungi Employee</h1>
      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="mb-5">
          <label htmlFor="first_name" className="block text-gray-700 text-lg font-medium">First Name</label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-5">
          <label htmlFor="last_name" className="block text-gray-700 text-lg font-medium">Last Name</label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-5">
          <label htmlFor="DOB" className="block text-gray-700 text-lg font-medium">Date of Birth</label>
          <input
            type="date"
            id="DOB"
            name="DOB"
            value={formData.DOB}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-5">
          <label htmlFor="salary" className="block text-gray-700 text-lg font-medium">Salary</label>
          <input
            type="number"
            id="salary"
            name="salary"
            value={formData.salary}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-5">
          <label htmlFor="fiscalCode" className="block text-gray-700 text-lg font-medium">Fiscal Code</label>
          <input
            type="text"
            id="fiscalCode"
            name="fiscalCode"
            value={formData.fiscalCode}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-5">
          <label htmlFor="email" className="block text-gray-700 text-lg font-medium">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
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
            {types.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>
        <div className="mb-5">
          <label htmlFor="hiring_date" className="block text-gray-700 text-lg font-medium">Hiring Date</label>
          <input
            type="date"
            id="hiring_date"
            name="hiring_date"
            value={formData.hiring_date}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-5">
          <label htmlFor="end_contract_date" className="block text-gray-700 text-lg font-medium">End Contract Date</label>
          <input
            type="date"
            id="end_contract_date"
            name="end_contract_date"
            value={formData.end_contract_date}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-5">
          <label htmlFor="attachments_uuid" className="block text-gray-700 text-lg font-medium">Attachments UUID</label>
          <input
            type="text"
            id="attachments_uuid"
            name="attachments_uuid"
            value={formData.attachments_uuid}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          type="submit"
          className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 col-span-2"
        >
          Submit
        </button>
        {isSuccess && <p className="text-green-500 mt-4 col-span-2">Employee added successfully!</p>}
      </form>
    </div>
  );
};

export default EmployeeForm;
