
'use client';
import React, { useCallback } from 'react';
import Modal from 'react-modal';
import { useRouter } from 'next/navigation';
const modalStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    transform: 'translate(-50%, -50%)',
    borderRadius: '8px',
    padding: '20px',
    width: '400px',
    maxWidth: '90%',
  },
};
interface FilterModalProps {
  isOpen: boolean;
  onClose: () => void;
  filters: {
    orderBy: string;
    name: string;
    description: string;
    province: string;
    city: string;
  };
  onFilterChange: (newFilters: Partial<{
    orderBy: string;
    name: string;
    description: string;
    province: string;
    city: string;
  }>) => void;
  onApplyFilters: () => void;
}

const FilterModal: React.FC<FilterModalProps> = ({ isOpen, onClose, filters, onFilterChange, onApplyFilters }) => {
  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    onFilterChange({ [name]: value });
  }, [onFilterChange]);

  const handleApplyFilters = useCallback(() => {
    
    onApplyFilters(); // Applica i filtri
    onClose(); // Chiudi il popup dopo aver applicato i filtri
  }, [onApplyFilters, onClose]);

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      style={modalStyles}
      contentLabel="Filter Modal"
    >
      <h2 className="text-xl font-bold mb-4">Filters</h2>
      <form>
        <label>
          Order By:
          <input
            type="text"
            name="orderBy"
            value={filters.orderBy}
            onChange={handleChange}
            placeholder="e.g., name,-province"
          />
        </label>
        <label>
          Name:
          <input
            type="text"
            name="name"
            value={filters.name}
            onChange={handleChange}
            placeholder="Name"
          />
        </label>
        <label>
          Description:
          <input
            type="text"
            name="description"
            value={filters.description}
            onChange={handleChange}
            placeholder="Description"
          />
        </label>
        <label>
          Province:
          <input
            type="text"
            name="province"
            value={filters.province}
            onChange={handleChange}
            placeholder="Province"
          />
        </label>
        <label>
          City:
          <input
            type="text"
            name="city"
            value={filters.city}
            onChange={handleChange}
            placeholder="City"
          />
        </label>
        <button
          type="button"
          onClick={handleApplyFilters}
          className="mt-4 py-2 px-4 bg-blue-500 text-white rounded"
        >
          Apply Filters
        </button>
        <button
          type="button"
          onClick={onClose}
          className="mt-4 py-2 px-4 ml-2 border rounded"
        >
          Cancel
        </button>
      </form>
    </Modal>
  );
};

export default FilterModal;
