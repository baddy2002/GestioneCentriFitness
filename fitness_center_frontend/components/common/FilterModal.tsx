'use client';
import React, { useCallback } from 'react';
import Modal from 'react-modal';

// Stili del modal
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

// Definizione dei tipi per i filtri
interface FilterField {
  label: string;
  name: string;
  placeholder: string;
}

interface FilterModalProps<T> {
  isOpen: boolean;
  onClose: () => void;
  filters: T;
  onFilterChange: (newFilters: Partial<T>) => void;
  onApplyFilters: () => void;
  filterFields: FilterField[];
}

const FilterModal = <T,>({
  isOpen,
  onClose,
  filters,
  onFilterChange,
  onApplyFilters,
  filterFields
}: FilterModalProps<T>) => {
  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    onFilterChange({ [name]: value } as Partial<T>);
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
        {filterFields.map(({ label, name, placeholder }) => (
          <label key={name}>
            {label}:
            <input
              type="text"
              name={name}
              value={(filters[name as keyof T] || '') as string} // Aggiunto || '' per evitare errori
              onChange={handleChange}
              placeholder={placeholder}
            />
          </label>
        ))}
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
