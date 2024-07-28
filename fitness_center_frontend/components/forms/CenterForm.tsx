// components/CenterForm.tsx

import React, { useState } from 'react';

const provinces = [
  'AG', 'AL', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AT', 'AV', 'BA', 'BT', 'BL',
  'BN', 'BG', 'BI', 'BO', 'BZ', 'BR', 'BS', 'BU', 'CA', 'CB', 'CE', 'CT',
  'CZ', 'FC', 'FE', 'FM', 'FR', 'GE', 'GO', 'GR', 'IM', 'IS', 'KR', 'LC',
  'LE', 'LI', 'LO', 'LT', 'LU', 'MC', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT',
  'NA', 'NO', 'NU', 'OG', 'OT', 'PA', 'PC', 'PD', 'PE', 'PG', 'PI', 'PN',
  'PO', 'PR', 'PT', 'PU', 'PZ', 'RA', 'RE', 'RI', 'RM', 'RO', 'SA', 'SI',
  'SJ', 'SR', 'SS', 'SV', 'TA', 'TE', 'TN', 'TO', 'TP', 'TR', 'TV', 'TS',
  'UD', 'VA', 'VE', 'VI', 'VR', 'VT', 'VS', 'VV'
];

const CenterForm: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    provincia: '',
    city: '',
    via: '',
    house_number: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(formData);
    // Handle form submission (e.g., send data to API or server)
  };

  return (
    <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-6 text-center">Aggiungi Centro</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-5">
          <label htmlFor="name" className="block text-gray-700 text-lg font-medium">Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
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
          <label htmlFor="provincia" className="block text-gray-700 text-lg font-medium">Provincia</label>
          <select
            id="provincia"
            name="provincia"
            value={formData.provincia}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="">Select Provincia</option>
            {provinces.map(prov => (
              <option key={prov} value={prov}>{prov}</option>
            ))}
          </select>
        </div>
        <div className="mb-5">
          <label htmlFor="city" className="block text-gray-700 text-lg font-medium">City</label>
          <input
            type="text"
            id="city"
            name="city"
            value={formData.city}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-5">
          <label htmlFor="via" className="block text-gray-700 text-lg font-medium">Via</label>
          <input
            type="text"
            id="via"
            name="via"
            value={formData.via}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-5">
          <label htmlFor="house_number" className="block text-gray-700 text-lg font-medium">House Number</label>
          <input
            type="number"
            id="house_number"
            name="house_number"
            value={formData.house_number}
            onChange={handleChange}
            className="mt-1 p-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <button
          type="submit"
          className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default CenterForm;
