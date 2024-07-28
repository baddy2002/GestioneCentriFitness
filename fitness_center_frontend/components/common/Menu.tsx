'use client';
import React from 'react';
import Modal from 'react-modal';

export type UserRole = 'admin' | 'manager' | 'nutritionist' | 'trainer' | 'customer';

export interface MenuItem {
  text: string;
  href?: string;
  requiredRole?: UserRole[];
  action?: () => void;
}

interface Props {
  roles: UserRole[];
  menuItems: MenuItem[];
}

const Menu: React.FC<Props> = ({ roles, menuItems }) => {
  const [modalIsOpen, setModalIsOpen] = React.useState(false);

  const canViewItem = (item: MenuItem) => {
    if (roles.includes('admin')) {
      return true;
    }
    if (item.requiredRole) {
      return item.requiredRole.some(role => roles.includes(role));
    }
    return false;
  };

  const handleClick = (action?: () => void, href?: string) => {
    if (action) {
      action();
    } else if (href) {
      window.location.href = href;
    }
  };

  return (
    <>
      <aside className="w-64 bg-gray-800 text-white flex-none">
        <div className="p-4">
          <h2 className="text-xl font-bold">Menu</h2>
          <ul className="mt-4">
            {menuItems
              .filter(canViewItem)
              .map((item, index) => (
                <li key={index}>
                  <button
                    onClick={() => handleClick(item.action, item.href)}
                    className="block py-2 px-4 text-left hover:bg-gray-700 w-full"
                  >
                    {item.text}
                  </button>
                </li>
              ))}
          </ul>
        </div>
      </aside>

      {/* Popup dei filtri */}
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={() => setModalIsOpen(false)}
        style={{
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
        }}
        contentLabel="Filter Modal"
      >
        <h2 className="text-xl font-bold mb-4">Filters</h2>
        {/* Placeholder per il contenuto del filtro */}
        <button
          onClick={() => setModalIsOpen(false)}
          className="mt-4 py-2 px-4 bg-blue-500 text-white rounded"
        >
          Close
        </button>
      </Modal>
    </>
  );
};

export default Menu;
